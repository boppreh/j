import webbrowser, urllib2
webbrowser.open('http://grooveshark.com/#!/search?q=' +
                urllib2.quote(raw_input()))
