import win32clipboard

win32clipboard.OpenClipboard()

try:
    directory = win32clipboard.GetClipboardData()
except:
    directory = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)[0]

from switcher import switch
switch(directory)
    
win32clipboard.CloseClipboard()

