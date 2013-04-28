import webbrowser, urllib2
webbrowser.open('https://encrypted.google.com/search?tbm=isch&q=' +
                urllib2.quote(raw_input()))
