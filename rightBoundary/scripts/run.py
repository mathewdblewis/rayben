# run this script like so:
# python3 run.py ../origin 2.37e5 3.16e0 .125 20 800 32



from math import log; import h5py; import os; from os import system; from sys import argv

def run(Ra,Pr,res,stop,Lx,newrun=False):
    system('mpiexec -n 4 python3 ../scripts/rayben.py %s %s %s %s %s %s' % (Ra,Pr,res,stop,Lx,'x' if newrun else ' '))
    pass


##  INPUT PARAMETERS:
if len(argv)!=8:
    print('input: origin, destRa, destPr, minStep, timeStep, longRun, newres')
    exit(1)

origin, newres = argv[1], int(argv[7])
destRa, destPr, minStep, timeStep, longRun = [float(t) for t in argv[2:7]]


# get initial state
latest = max([int(t.split('_s')[1].split('.')[0]) for t in os.listdir('%s/checkpoints' % origin) if t[-3:]=='.h5'])
system('mkdir checkpoints; cp -R %s/checkpoints/checkpoints_s%d* checkpoints' % (origin,latest))

# extract params
file = h5py.File('checkpoints/checkpoints_s%d.h5' % latest, mode='r')
F = file['tasks']
Ra,Pr,Lx,res = [round(t[0][0][0],3) for t in [F['myRa'],F['myPr'],F['myLx'],F['myRes']]]
stopTime = file['scales/sim_time'][-1]

# set the new resolution if desired
if newres!=0: res=newres

# travel towards the destination
while True:
    # travel towards the destination
    if    Ra<destRa/10**minStep: Ra*=10**minStep
    elif  Ra>destRa*10**minStep: Ra/=10**minStep
    else: Ra = destRa
    if    Pr<destPr/10**minStep: Pr*=10**minStep
    elif  Pr>destPr*10**minStep: Pr/=10**minStep
    else: Pr = destPr
    if (Ra,Pr) == (destRa,destPr): break
    print('\n***** log(Ra)=%s,log(destRa)=%s *****\n' % (log(Ra),log(destRa)))
    # simulate for the correct amount of time
    stopTime += timeStep
    run(Ra,Pr,res,stopTime,Lx)

# run for a long time
stopTime += longRun
run(Ra,Pr,res,stopTime,Lx)






