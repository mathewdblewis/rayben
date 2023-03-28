from os import system

rate = .001

cmd = 'mpiexec -n 4 python3 ../scripts/rayben.py %+3f %+3f %.3f 32 6000 20 &'
RaPr = ((3.000,-1.750),(4.000,-1.250),(4.250,-1.250))

n = 3
d = .25

n -= 1
for r in RaPr:
	x,y = r[1]-n*d+d,r[1]-n*d
	C = cmd % (r[0],y,rate)
	# system('mkdir RaPr%+.3f,%+.3f_' % (r[0],y))
	# system('cp -R RaPr%+.3f,%+.3f_/checkpoints RaPr%+.3f,%+.3f_' % (r[0],x,r[0],y))
	open('RaPr%+.3f,%+.3f_/run.sh' % (r[0],y),'w').write(C)
	system('chmod 777 RaPr%+.3f,%+.3f_/run.sh' % (r[0],y))
	system('cd RaPr%+.3f,%+.3f_; ./run.sh' % (r[0],y))


