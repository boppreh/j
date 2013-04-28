import webbrowser, urllib2
webbrowser.open('https://encrypted.google.com/search?q=' +
                urllib2.quote(raw_input()))
