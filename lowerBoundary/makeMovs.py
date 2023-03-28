from os import system

RaPr = ((3.000,-1.250),(3.250,-1.000),(3.500,-1.000),(3.750,-1.000),(4.000,-0.750),(4.250,-0.750),(4.500,-0.500),(4.750,-0.500),(5.000,-0.250),(5.250,-0.250),(5.500,0.000),(5.750,-0.000))


for r in [0]:
    for x in RaPr:
        d = 'RaPr%+.3f,%+.3f_' % (x[0],x[1]-r)
        # system('ls %s/movie.mov > temp' % d)
        # if open('temp','r').read() == '':
        system('cd %s; python3 ../scripts/makeMovFromFrames.py' % d)
        # system('rm temp')



