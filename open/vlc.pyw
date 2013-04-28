import subprocess
try:
    subprocess.Popen(r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe')
except:
    subprocess.Popen(r'G:\VLC\vlc.exe')
