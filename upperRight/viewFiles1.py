from os import system

system('ls RaPr* > temp.temp')
x = open('temp.temp','r').read()
system('rm temp.temp')
RaPr = [tuple([float(q) for q in t[4:-2].split(',')]) for t in x.split('\n') if len(t)>0 and t[-1]==':']


for x in RaPr:
	system('open `ls RaPr%+.3f,%+.3f_/frames/* | tail -1`' % x)


