from os import system

for x in range(15):
	system('open `ls RaPr%+.3f,%+.3f_/frames/* | tail -1`' % (5.75,x/4))


