import os
name = raw_input()
directory = r'M:\musics\source'
l = [source for source in os.listdir(directory) if name in source.lower()]
if not l:
    exit()

from subprocess import Popen
Popen([r'G:\VLC\vlc.exe', '--qt-start-minimized'] + l, cwd=directory)
