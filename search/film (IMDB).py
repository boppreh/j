import webbrowser, urllib2
webbrowser.open('http://www.imdb.com/find?s=all&q=' +
                urllib2.quote(raw_input()))
