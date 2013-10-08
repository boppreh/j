import webbrowser, urllib2
webbrowser.open('http://localhost:5000/?q=' + urllib2.quote(raw_input()))
