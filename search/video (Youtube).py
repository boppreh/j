import webbrowser, urllib2
webbrowser.open('https://www.youtube.com/results?search_query=' +
                urllib2.quote(raw_input()))
