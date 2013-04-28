import webbrowser, urllib2

webbrowser.open('https://en.wikipedia.org/wiki/Special:Search?fulltext=Search&search=' +
                urllib2.quote(raw_input()))
