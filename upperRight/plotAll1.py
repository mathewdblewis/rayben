from os import system

# system('ls RaPr* > temp.temp')
# x = open('temp.temp','r').read()
# RaPr = [tuple([float(q) for q in t[4:-2].split(',')]) for t in x.split('\n') if len(t)>0 and t[-1]==':']
# print(RaPr)


for x in range(15):
	system('cd RaPr%+.3f,%+.3f_; python3 ../scripts/plot.py snapshots/*.h5 &' % (5.75,x/4))



