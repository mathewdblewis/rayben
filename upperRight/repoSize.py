from os import system

system('wc -c */checkpoints/*.h5 */checkpoints/*/*.h5 | tail -1 > temp.temp')
x = float(open('temp.temp','r').read().split(' ')[0])/10**9
print('h5 files:\t%.3f gigs' % x)
system('rm temp.temp')

system('wc -c */mov* | tail -1 > temp.temp')
x = float(open('temp.temp','r').read().split(' ')[0])/10**9
print('movies:\t\t%.3f gigs' % x)
system('rm temp.temp')




