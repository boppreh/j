import webbrowser, urllib2
webbrowser.open('https://mail.google.com/mail/u/0/?shva=1#search/' +
                urllib2.quote(raw_input()))
