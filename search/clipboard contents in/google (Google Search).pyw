import webbrowser, urllib2, win32clipboard

win32clipboard.OpenClipboard()

for search_term in win32clipboard.GetClipboardData().split('\n'):
    if not search_term.isspace():
        webbrowser.open('https://encrypted.google.com/search?q=' +
                        urllib2.quote(search_term))

win32clipboard.CloseClipboard()
