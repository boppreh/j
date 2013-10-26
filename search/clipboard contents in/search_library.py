from urllib.parse import quote
import webbrowser
import win32clipboard

def open_search(url_template, prefix=''):
    if not '{}' in url_template:
        url_template += '{}'

    win32clipboard.OpenClipboard()

    for search_term in win32clipboard.GetClipboardData().split('\n'):
        if not search_term.isspace():
            webbrowser.open(url_template.format(quote(prefix + search_term)))

    win32clipboard.CloseClipboard()
