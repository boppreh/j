from urllib.parse import quote
import webbrowser
webbrowser.open('https://encrypted.google.com/search?q=' + 
                quote(input()) + '&btnI')
