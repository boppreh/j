import telnetlib
tn = telnetlib.Telnet('localhost', 4212)
tn.read_until(':')
tn.write('admin\n')
tn.write('pause\n')
