from os import system

cmd = 'python3 ../scripts/rayben.py %+3f %+3f .001 32 10000 20 &'

s = 4

s -= 2
for i in range(15):
    x,y = (5.5+s/4,i/4),(5.75+s/4,i/4)
    d1 = 'RaPr%+.3f,%+.3f_' % x
    d2 = 'RaPr%+.3f,%+.3f_' % y
    system('mkdir %s; mkdir %s/checkpoints' % (d2,d2))
    system('cp -R %s/checkpoints/* %s/checkpoints' % (d1,d2))
    open('%s/run.sh' % d2,'w').write(cmd % y)
    system('chmod 777 %s/run.sh' % d2)
    system('cd %s; ./run.sh' % d2)




