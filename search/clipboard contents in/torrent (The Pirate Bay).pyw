import webbrowser, urllib2, win32clipboard

win32clipboard.OpenClipboard()

for search_term in win32clipboard.GetClipboardData().split('\n'):
    if not search_term.isspace():
        webbrowser.open('https://thepiratebay.se/search/' +
                        urllib2.quote(search_term) + '/0/7/0')

win32clipboard.CloseClipboard()
