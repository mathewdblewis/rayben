from os import system


for Ra in [5.75,6,6.25]:
    for x in range(15):
        system('cd RaPr%+.3f,%+.3f_; python3 ../scripts/makeMovFromFrames.py' % (Ra,x/4))



