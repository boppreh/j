import win32clipboard
import subprocess
import os

from win32com.shell import shell, shellcon
directory = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0)

filename = raw_input()
path = os.path.join(directory, filename)

win32clipboard.OpenClipboard()
open(path, 'w').write(win32clipboard.GetClipboardData())
subprocess.Popen('G:/Vim/vim73/gvim.exe ' + path)
win32clipboard.CloseClipboard()
