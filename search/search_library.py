from urllib.parse import quote
import webbrowser

def open_search(url_template, prefix=''):
    if not '{}' in url_template:
        url_template += '{}'
    webbrowser.open(url_template.format(quote(prefix + input())))

