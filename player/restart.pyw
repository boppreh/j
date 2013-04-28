import telnetlib
tn = telnetlib.Telnet('localhost', 4212)
tn.read_until(':')
tn.write('admin\n')
tn.write('seek 0\n')
tn.write('play\n')
