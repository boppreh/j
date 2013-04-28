import webbrowser, urllib2
webbrowser.open('https://www.wolframalpha.com/input/?i=' +
                urllib2.quote(raw_input()))
