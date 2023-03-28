from os import system

system('ls Ra* > temp.temp')
D = [t[:-1] for t in open('temp.temp','r').read().split('\n') if t!='' and t[-2:]=='_:'][0]
system('open %s/movie.mov' % D)
label = ''

while label not in ['varient','invarient','breaks','unique']: label = input('label: ')
system('mv %s %s%s' % (D,D,label))


