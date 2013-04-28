import webbrowser, urllib2

webbrowser.open('https://maps.google.com/maps?q=' + urllib2.quote(raw_input()))
