from os import system

rate = .001

cmd = 'python3 ../scripts/rayben.py %+3f %+3f %.3f 32 7000 20 &'
RaPr = ((3.000,-1.250),(3.250,-1.000),(3.500,-1.000),(3.750,-1.000),(4.000,-0.750),(4.250,-0.750),\
	(4.500,-0.500),(4.750,-0.500),(5.000,-0.250),(5.250,-0.250),(5.500,0.000),(5.750,-0.000))

n = 3
d = .25

n -= 1
for r in RaPr:
	x,y = r[1]-n*d+d,r[1]-n*d
	C = cmd % (r[0],y,rate)
	system('ls -lR RaPr%+.3f,%+.3f_* > temp.temp' % (r[0],y))
	file = open('temp.temp','r').read().split('\n')[0][:-1]
	open('%s/run.sh' % file,'w').write(C)
	system('cd %s; ./run.sh' % file)

system('rm temp.temp')


