from win32com.shell import shell, shellcon
from os import path

def switch(new_location):
    assert path.isdir(new_location)
    shell.SHSetFolderPath(shellcon.CSIDL_DESKTOP, new_location, 0)
    shell.SHChangeNotify(shellcon.SHCNE_ASSOCCHANGED,
                         shellcon.SHCNF_IDLIST,
                         [], [])
