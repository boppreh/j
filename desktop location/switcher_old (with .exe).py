from subprocess import Popen

def switch(new_location):
    Popen(r'J:\switcher.exe "' + new_location + '"', shell=True)
