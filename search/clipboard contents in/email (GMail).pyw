import webbrowser, urllib2, win32clipboard

win32clipboard.OpenClipboard()

for search_term in win32clipboard.GetClipboardData().split('\n'):
    if not search_term.isspace():
        webbrowser.open('https://mail.google.com/mail/u/0/?shva=1#search/' +
                        urllib2.quote(search_term))

win32clipboard.CloseClipboard()