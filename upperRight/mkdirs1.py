from os import system

cmd = 'python3 ../scripts/rayben.py %+3f %+3f .002 32 6000 20 &'

for i in range(15):
    x = (5.5,i/4)
    d = 'RaPr%+.3f,%+.3f_' % x
    system('mkdir %s; mkdir %s/checkpoints' % (d,d))
    system('cp -R checkpoints/checkpoints_s%d* %s/checkpoints' % (357+40*i,d))
    system('cp -R checkpoints/checkpoints_s%d* %s/checkpoints' % (358+40*i,d))
    open('%s/run.sh' % d,'w').write(cmd % x)
    system('chmod 777 RaPr%+.3f,%+.3f_/run.sh' % x)
    system('cd RaPr%+.3f,%+.3f_; ./run.sh' % x)





