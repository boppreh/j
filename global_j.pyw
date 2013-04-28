import os
from subprocess import Popen
from background import tray, notify, register_many_hotkeys
import string

tray('J', 'j.ico')

class J(object):
    def __init__(self):
        self.path = '.'

    def _execute(self):
        assert os.path.isfile(self.path)

        full_path = '"' + os.path.abspath(self.path) + '"'

        if full_path.endswith('.pyw'):
            Popen('pythonw ' + full_path, shell=True)
        elif full_path.endswith('.py'):
            os.system('python ' + full_path)
        else:
            os.startfile(full_path)

    def next(self, letter):
        try:

            folder_items = os.listdir(self.path)
            names = [name for name in folder_items if name.startswith(letter)]

            if names:
                self.path += '/' + names[0]
                if os.path.isfile(self.path):
                    self._execute()

            if not os.path.isdir(self.path):
                self.path = '.'

        except Exception as e:
            notify('Error', e.message)
            print e
            with open('errors.txt', 'a') as file:
                file.write(str(e) + '\n\n')

j = J()

def make_callback(letter):
    return lambda: j.next(letter)

hotkeys = [(c, make_callback(c)) for c in string.lowercase]

register_many_hotkeys(hotkeys, alt=True, ctrl=True)
#user32.UnregisterHotKey(None, j)
