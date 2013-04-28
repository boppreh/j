import win32clipboard

win32clipboard.OpenClipboard()

try:
    html = win32clipboard.GetClipboardData(win32clipboard.RegisterClipboardFormat("HTML Format"))
    import re, webbrowser
    for match in re.finditer('href="(.+?)"', html):
        webbrowser.open(match.groups()[0])
except:
    import os
    try:
        for address in win32clipboard.GetClipboardData().split('\n'):
            if len(address) > 3:
                os.startfile(address)
    except:
        for filename in win32clipboard.GetClipboardData(win32clipboard.CF_HDROP):
            os.startfile(filename)
    
win32clipboard.CloseClipboard()

