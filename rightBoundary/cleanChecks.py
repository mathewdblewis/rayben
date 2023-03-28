from os import system

system('ls RaPr* > temp.temp')
Q = [t[:-1] for t in open('temp.temp','r').read().split('\n') if t !='' and t[-1] == ':']
for q in Q:
	system('ls %s/checkpoints/* > temp.temp' % q)
	X = [t[:-1] for t in open('temp.temp','r').read().split('\n') if t !='' and t[-1] == ':']
	X = [t[1] for t in sorted([(int(x.split('_s')[1]),x) for x in X])[:-2]]
	for x in X:
		system('rm -rf %s.h5 %s/' % (x,x))
system('rm temp.temp')

