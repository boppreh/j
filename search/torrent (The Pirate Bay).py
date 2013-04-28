import webbrowser, urllib2
webbrowser.open('https://thepiratebay.se/search/' + 
                urllib2.quote(raw_input()) + '/0/7/0')
