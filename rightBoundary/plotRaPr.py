from os import system
from matplotlib import pyplot as plt
system('ls > temp.temp')
x=[t[4:].split('_') for t in open('temp.temp','r').read().split('\n')[:-1] if t[:4]=='RaPr']
system('rm temp.temp')
A = [[float(q) for q in t[0].split(',')] for t in x if t[1]=='']
B = [[float(q) for q in t[0].split(',')] for t in x if t[1]=='breaks']
C = [[float(q) for q in t[0].split(',')] for t in x if t[1]=='invarient']
D = [[float(q) for q in t[0].split(',')] for t in x if t[1]=='varient']

Q = [(A,'unlabeled'),(B,'breaks'),(C,'invarient'),(D,'varient')]
[plt.scatter([x[0] for x in q[0]],[x[1] for x in q[0]],label=q[1]) for q in Q]

plt.legend()
plt.savefig('runs.png')


