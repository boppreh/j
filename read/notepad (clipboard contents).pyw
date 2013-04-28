import subprocess
import os
import time
open('vim command', 'w').write('"*P')
subprocess.Popen('G:/Vim/vim73/gvim.exe -s "vim command"')
time.sleep(0.5)
os.remove('vim command')
