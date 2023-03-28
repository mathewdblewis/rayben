from os import system
from matplotlib import pyplot as plt
system('ls > temp.temp')
x=[t[4:] for t in open('temp.temp','r').read().split('\n')[:-1] if t[:4]=='RaPr']
system('rm temp.temp')

L = ['','breaks','invarient','varient','unique']
Q = []
for label in L:Q += [([[float(q) for q in t[:-1].split(',')] for t in x if open('RaPr%s/label.txt'%t).read()==label],label)]
[plt.scatter([x[0] for x in q[0]],[x[1] for x in q[0]],label=q[1]) for q in Q]

plt.legend()
plt.savefig('runs.png')


