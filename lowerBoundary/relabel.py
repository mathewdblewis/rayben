from os import system

system('ls Ra* > temp')
X = [t[:-1] for t in open('temp','r').read().split('\n') if t !='' and t[-1]==':']
for x in X:
	d,lab = x.split('_')
	system('mv %s %s_' % (x,d))
	open('%s/label.txt' % x,'w').write(lab)


