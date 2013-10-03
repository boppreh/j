import os
from subprocess import Popen
from background import tray, notify
from keyboard import register_hotkey
from simpleserver import serve
import string

tray('J', 'j.ico')
serve({}, port=2344)

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

for letter in string.lowercase:
    register_hotkey('lcontrol+rmenu+' + letter, j.next, letter)

#user32.UnregisterHotKey(None, j)
