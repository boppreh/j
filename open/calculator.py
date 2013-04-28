from __future__ import division
import msvcrt, os
import re
from itertools import islice
from fractions import Fraction
import math

unit_abbreviations = {'ns': 'nanosecond',
                      'ms': 'millisecond',
                      's': 'second',
                      'min': 'minute',
                      'h': 'hour',

                      'mm': 'millimeter',
                      'm': 'meter',
                      'cm': 'centimeter',
                      'km': 'kilometer',

                      'mg': 'milligram',
                      'g': 'gram',
                      'kg': 'kilogram',

                      'b': 'byte',
                      'kb': 'kilobyte',
                      'mb': 'megabyte',
                      'gb': 'gigabyte',
                      'tb': 'terabyte',
                      }

# When adding new values, try to keep a linear flow of units.
# Circular dependencies may lock a group of units out of use, so please define
# each unit in terms of the preceding (if it's bigger) or next (if it's
# smaller). Units defined in terms of themselves (1 second = 1 second) are used
# to identify the preferred formats, so it's important for the units to
# "converge".
unit_transformations = {'nanosecond': (1 / 1000, 'microsecond'),
                        'microsecond': (1 / 1000, 'millisecond'),
                        'millisecond': (1 / 1000, 'second'),
                        'second': (1, 'second'),
                        'minute': (60, 'second'),
                        'hour': (60, 'minute'),
                        'day': (24, 'hour'),
                        'week': (7, 'day'),
                        'month': (30, 'day'),
                        'year': (365, 'day'),
                        'decade': (10, 'year'),
                        'century': (100, 'year'),

                        'nanometer': (1 / 1000, 'micrometer'),
                        'micrometer': (1 / 1000, 'millimeter'),
                        'millimeter': (1 / 10, 'centimeter'),
                        'centimeter': (1 / 100, 'meter'),
                        'meter': (1, 'meter'),
                        'kilometer': (1000, 'meter'),

                        'milligram': (1 / 1000, 'gram'),
                        'gram': (1, 'gram'),
                        'kilogram': (1000, 'gram'),
                        'ton': (1000, 'kilogram'),

                        'bit': (1 / 8, 'byte'),
                        'byte': (1, 'byte'),
                        'kilobyte': (1000, 'byte'),
                        'megabyte': (1000, 'kilobyte'),
                        'gigabyte': (1000, 'megabyte'),
                        'terabyte': (1000, 'gigabyte'),
                       }

all_units = unit_transformations.keys() + unit_abbreviations.keys()

# Associates each unit with a prime number. This is used to simplify unit
# fractions using the fractions module.

# Naive prime generator. It is far from being a bottle-neck, so no need to
# optimize this yet.
primes_generator = (x for x in range(2, 999) if all(x % y for y in range(2, x)))
primes = list(islice(primes_generator, 0, len(all_units)))
assert len(primes) >= len(all_units)
unit_primes = dict(zip(all_units, primes))

def singular(unit_name):
    """
    Returns the singular of a given name. If the name is an abbreviation
    (found in unit_abbreviations), no change is made even if it ends in 's'.

    seconds -> second (removed s)
    kilometers -> kilometer (removed s)
    gram -> gram (no change because it was already singular)
    ms -> ms (no change because it was an abbreviation)
    """
    if unit_name in unit_abbreviations or not unit_name.endswith('s'):
        return unit_name
    elif unit_name.endswith('s'):
        return unit_name[:-1]

def make_value(unit_name):
    """
    Returns an instance of Value with value 1 and singular, not abbreviated
    unit. If an unknown unit name is provided, it is registered for further
    support.

    's' -> Value(1, 'second')
    'seconds' -> Value(1, 'second')
    'made_up_unit' -> Value(1, 'made_up_unit')
    """
    unit_name = singular(unit_name)

    if unit_name in unit_abbreviations:
        unit_name = unit_abbreviations[unit_name]
    elif unit_name not in unit_primes:
        # By associating the new unit name with a unique prime number, this
        # unit can be used in the simplification and minimization algorithm.
        unit_primes[unit_name] = primes_generator.next()

    return Value(1, ((unit_name,), ()))

def unit_to_fraction(unit):
    """
    Converts a unit, such as 'meter'/'second', in a fraction of prime numbers,
    such as 173/101. The goal of this function is to remove redundant units
    present in both numerator and denominator.
    """
    numerator = 1
    for unit_name in unit[0]:
        numerator *= unit_primes[unit_name]

    denominator = 1
    if len(unit) > 1:
        for unit_name in unit[1]:
            denominator *= unit_primes[unit_name]

    return Fraction(numerator, denominator)

def fraction_to_unit(fraction):
    """
    Converts a fraction of prime numbers back into a tuple of units.
    """
    numerator = []
    denominator = []

    for unit_name, prime in unit_primes.items():
        while fraction.numerator % prime == 0:
            # Even though the result is guaranteed to be a round number,
            # division now yields float values because of the __future__
            # import. If we don't convert the result back to int, Fraction
            # complains about the arguments not being Rational instances.
            fraction = Fraction(int(fraction.numerator / prime),
                                fraction.denominator)
            numerator.append(unit_name)

        # Exactly the same, but for the denominator. Didn't find an elegant way
        # to extract the logic.
        while fraction.denominator % prime == 0:
            fraction = Fraction(fraction.numerator,
                                int(fraction.denominator / prime))
            denominator.append(unit_name)

    return (tuple(numerator), tuple(denominator))

def simplify(unit):
    """
    Removes redundant sub-units by simplifying numerator with denominator.

    (('meter',), ('meter', 'second') -> ((), 'second')
    (('meter', 'meter'), ('meter', 'second') -> (('meter',), ('second',))
    """
    simplified_fraction = unit_to_fraction(unit).limit_denominator()
    return fraction_to_unit(simplified_fraction)

def get_preferred_unit(unit_name):
    """
    Runs unit_name through unit_transformations as many times as possible until
    equilibrium is reached (i.e. the preferred unit is reached), returning the
    scale difference and name of the final unit. Unknown units are returned as
    is with scale 1.

    Example:

    made_up_unit (?) -> 1, made_up_unit
    meter (meter -> meter) -> 1, meter
    kilometer (kilometer -> meter -> meter) -> 1000, meter
    megabyte (megabyte -> kilobyte -> byte -> byte) -> 1000000, byte
    """
    if unit_name not in unit_transformations:
        return 1, unit_name

    multiplier = 1
    while unit_transformations[unit_name][1] != unit_name:
        unit_multiplier, unit_name = unit_transformations[unit_name]
        multiplier *= unit_multiplier

    return multiplier, unit_name

def get_relative_scale(src_unit_name, dst_unit_name):
    """
    Calculates the scale required to convert a value from src_unit_name to
    dst_unit_name.

    Example:

    'kilometer', 'meter' -> 1 / 1000
    'kilobyte', 'bit' -> 8 / 1000
    'kilobyte', 'meter' -> assertion error
    """
    src_absolute_scale, src_absolute_name = get_preferred_unit(src_unit_name)
    dst_absolute_scale, dst_absolute_name = get_preferred_unit(dst_unit_name)

    assert src_absolute_name == dst_absolute_name

    return src_absolute_scale / dst_absolute_scale

def convert(value, unit, new_unit):
    """
    Converts a value from one unit to another. Returns the new value by itself.
    """
    for src_unit_name, dst_unit_name in zip(unit[0], new_unit[0]):
        value *= get_relative_scale(src_unit_name, dst_unit_name)

    for src_unit_name, dst_unit_name in zip(unit[1], new_unit[1]):
        value /= get_relative_scale(src_unit_name, dst_unit_name)

    return value

def normalize(value, unit):
    """
    Converts a given value and unit to the preferred sub units, returning the
    new scaled value and unit name. The goal is to convert all values with
    compatible units to the exact same unit by scaling the value.

    Example:

    1, (('meter,'), ()) -> 1, (('meter,'), ())
    1, (('kilometer,'), ()) -> 1000, (('meter,'), ())
    1, (('kilometer,'), ('hour',)) -> 0.277778, (('meter,'), ('second',))
    """
    numerator = (get_preferred_unit(unit_name)[1] for unit_name in unit[0])
    denominator = (get_preferred_unit(unit_name)[1] for unit_name in unit[1])
    preferred = (tuple(numerator), tuple(denominator))
    return convert(value, unit, preferred), preferred

def get_most_natural(value_name_pairs):
    """
    Returns the value/name pair with log10 nearest to 1. log10 gives an
    unusually good approximation for how "simple" a value is, measuring 10 and
    0.1 as the same distance from 1.
    """
    return sorted(value_name_pairs, key=lambda x: abs(math.log10(x[0])))[0]

def get_minimized_value(value, unit_name, inverse_scale=False):
    """
    Runs the value through all possible unit transformations to find the one
    that yields the value nearest to 1 (as measured in log10 scale).

    Example:

    1, 'meter' -> 1, 'meter'
    1000, 'meter' -> 1, 'kilometer'
    0.05, 'meter' -> 5, 'centimeter'
    """
    # Ignore unknown units.
    if unit_name not in unit_transformations or value == 0:
        return value, unit_name

    alternatives = []
    for converted_name in unit_transformations:
        try:
            scale = get_relative_scale(unit_name, converted_name)
        except:
            continue

        if inverse_scale:
            converted_value = value / scale
        else:
            converted_value = value * scale

        alternatives.append((converted_value, converted_name))

    return get_most_natural(alternatives)

def minimize(value, unit):
    """
    Converts value and unit to the unit that gives the smallest value 
    (nearest to 1, measured in log10).

    Example:

    1, (('meter'), ()) -> 1, (('meter'), ())
    1000, (('meter'), ()) -> 1, (('kilometer'), ())
    10, (('meter'), ('hour')) -> 0.41666, (('meter',), ('day'))
    100, ((), ('day')) -> 0.3472, ((), ('year'))
    """
    if (not unit[0] and not unit[1]) or value == 0:
        return value, unit

    alternatives = []

    for i, unit_name in enumerate(unit[0]):
        new_value, new_unit_name = get_minimized_value(value, unit_name)
        new_unit = (unit[0][:i] + (new_unit_name,) + unit[0][i+1:], unit[1])
        alternatives.append((new_value, new_unit))

    # Don't try to simplify denominators for now.
    #for i, unit_name in enumerate(unit[1]):
    #    new_value, new_unit_name = get_minimized_value(value, unit_name)
    #    new_unit = (unit[0], unit[1][:i] + (new_unit_name,) + unit[1][i+1:])
    #    alternatives.append((new_value, new_unit))

    return get_most_natural(alternatives)

class Value(object):
    """
    Immutable class for representing a pair value, unit. The value itself is a
    float number, while the unit is a nested tuple containing strings. This
    class has support for common arithmetic operations and string conversion.

    Units are represented as follows:

    ((numerator1, numerator2, ...), (denominator1, denominator2, ...))

    Example:

    meter -> (('meter',), ())
    meter / second -> (('meter',), ('second',))
    meter^2 -> (('meter', 'meter'), ())
    meter / second^2 -> (('meter',), ('second', 'second'))
    meter^2 / second^2 -> (('meter', 'meter'), ('second', 'second))
    """
    def __init__(self, value, unit):
        """
        Creates a new Value object with a given value and unit. The unit is
        normalized and simplified.
        """
        assert type(unit) == tuple and len(unit) == 2
        self.value, self.unit = normalize(value, simplify(unit))

    def _operate(self, operation, other, right_side):
        """
        Applies an operation to this instance.

        operation: a two argument function that operates on numbers.
        other: the other number or Value.
        right_side: bool representing if the current instance is on the right
        side of the operation (and thus the operation must be reversed)
        """
        # Reverses provided operation when on the right side.
        op = (lambda x, y: operation(y, x)) if right_side else operation

        # Regular number operation, maintaining unit.
        if type(other) != Value:
            return Value(op(self.value, other),
                         self.unit)

        if operation in (add, sub):
            assert other.unit == self.unit
            return Value(op(self.value, other.value), self.unit)

        else:
            assert operation in (mul, div)

            if operation == mul:
                other_unit = other.unit
            else:
                other_unit = (other.unit[1], other.unit[0])

            unit = (self.unit[0] + other_unit[0], self.unit[1] + other_unit[1])

            return Value(op(self.value, other.value), unit)

    def __add__(self, other): return self._operate(add, other, False) 
    def __sub__(self, other): return self._operate(sub, other, False) 
    def __mul__(self, other): return self._operate(mul, other, False)
    def __div__(self, other): return self._operate(div, other, False)
    def __truediv__(self, other): return self._operate(div, other, False)

    def __radd__(self, other): return self._operate(add, other, True) 
    def __rsub__(self, other): return self._operate(rsub, other, True) 
    def __rmul__(self, other): return self._operate(mul, other, True)
    def __rdiv__(self, other): return self._operate(div, other, True)
    def __rtruediv__(self, other): return self._operate(div, other, True)

    def __eq__(self, other):
        """ Compares a number of another value to this instance. """
        if type(other) != Value:
            # A value may be equal to a raw number if all its units have been
            # simplified away.
            return not self.unit[0] and not self.unit[1] and self.value == other
        else:
            return self.value == other.value and self.unit == other.unit

    def __str__(self):
        """
        Converts the value, unit pair to a string. The units are simplified and
        minimized to result in the smallest value possible.
        """
        value, unit = minimize(self.value, simplify(self.unit))
        if value > 10**10:
            value = float(value)
        elif value == int(value):
            value = int(value)

        str_unit = ' '.join(unit[0])
        if unit[1]:
            str_unit += ' / ' + ' '.join(unit[1]) if unit[1] else ''

        return str(value) + ' ' + str_unit

# Make the most common libraries available by default.
from re import *
from os.path import *
from os import *
from math import *
from collections import *
from itertools import *
from string import *
from random import *
from operator import *

# The operator module already contains a div function, but we must create our
# own to work with "from __future__ import division".
div = lambda x, y: x / y

# Create global variables for each unit name.
for unit_abbreviation, unit_name in unit_abbreviations.items():
    exec(unit_abbreviation + '= make_value("' + unit_name + '")')
for unit_name in unit_transformations:
    exec(unit_name + '= make_value("' + unit_name + '")')

# Characters before cursor.
before = []
# Characters after cursor.
after = []
# Last valid expression result, used while the current expression has an error.
last_result = None

while True:
    char = msvcrt.getch()

    # Ignore non-ascii characters, they are probably control symbols.
    if ord(char) > 128:
        continue

    if ord(char) == 8: # Backspace.
        if len(before):
            before.pop()
    elif ord(char) == 83: # Delete.
        if len(after):
            after.pop(0)
    elif ord(char) == 75: # Left arrow.
        if len(before):
            after.insert(0, before.pop())
    elif ord(char) == 77: # Right arrow.
        if len(after):
            before.append(after.pop(0))
    elif ord(char) == 79: # Home.
        before = before + after
        after = []
    elif ord(char) == 71: # End.
        after = before + after
        before = []
    elif char not in ('\t', '\n', '\r'): # Ignore line breaks and tabs.
        before.append(char)

    os.system('cls')
    expression = ''.join(before + after)
    print expression
    # Print a ^ to show the current caret position.
    print ' ' * len(before) + '^'
    try:
        last_result = eval(expression)

        # Print the help page of a function instead of the unhelpful
        # <function <xyz> at 0x00000>
        # Uses only the first 20 lines as to now hide the input expression.
        if callable(last_result):
            last_result = '\n'.join(last_result.__doc__.split('\n')[:20])
    except:
        # In case of syntax error, replace expressions of the form '1.5 word'
        # with '1.5 * make_value("word")' in order to support literal units.
        expression = re.sub('(\d*\.?\d+\s*)([a-zA-Z_]+?)(\W|$)',
                            r'(\1 * make_value("\2"))\3',
                            expression)
        try:
            last_result = eval(expression)
        except Exception as e:
            # If it still failed after replacing the units, just print the last
            # result.

            print last_result, '(Error)'
            print ''
            print e
            continue

    print last_result
