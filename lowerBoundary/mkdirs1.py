from os import system


cmd = 'python3 ../scripts/rayben.py %+3f %+3f .002 32 3000 20 &'
RaPr = ((3.000,-1.250),(3.250,-1.000),(3.500,-1.000),(3.750,-1.000),(4.000,-0.750),(4.250,-0.750),(4.500,-0.500),(4.750,-0.500),(5.000,-0.250),(5.250,-0.250),(5.500,0.000),(5.750,-0.000))

for x in RaPr:
	C = cmd % x
# 	system('mkdir RaPr%+.3f,%+.3f_' % x)
#	system('cp -R origin/checkpoints RaPr%+.3f,%+.3f_' % x)
	open('RaPr%+.3f,%+.3f_/run.sh' % x,'w').write(C)
	system('chmod 777 RaPr%+.3f,%+.3f_/run.sh' % x)
	system('cd RaPr%+.3f,%+.3f_; ./run.sh' % x)



