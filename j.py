import msvcrt, os

path = 'j'
try:
    while os.path.isdir(path):
        path += '/' + msvcrt.getch()
    execfile(path + '.py')
except Exception as e:
    print e
    raw_input()
