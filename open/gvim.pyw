import subprocess
for path in ['gvim',
             'C:/Program Files (x86)/Vim/vim73/gvim.exe',
             'G:/Vim/vim73/gvim.exe']:
    try:
        subprocess.Popen(path)
        break
    except:
        continue
