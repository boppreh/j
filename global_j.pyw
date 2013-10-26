import os
from subprocess import Popen
from tray import tray, notify
from keyboard import register_hotkey
from simpleserver import serve
import string

last_commands = []

tray('J', 'j.ico')
serve(last_commands, port=2344)

class J(object):
    def __init__(self):
        self.path = '.'
        self.letters = ''

    def _execute(self):
        assert os.path.isfile(self.path)

        last_commands.append(self.letters)
        if len(last_commands) > 50:
            last_commands.pop(0)

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
                self.letters += letter
                if os.path.isfile(self.path):
                    self._execute()

            if not os.path.isdir(self.path):
                self.path = '.'
                self.letters = ''

        except Exception as e:
            notify('Error', e.message)
            print(e)
            with open('errors.txt', 'a') as file:
                file.write(str(e) + '\n\n')

j = J()

for letter in string.ascii_lowercase:
    register_hotkey('lcontrol+rmenu+' + letter, j.next, letter)

#user32.UnregisterHotKey(None, j)
