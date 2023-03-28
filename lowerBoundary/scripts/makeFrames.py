import os
os.system('cp -R snapshots snaps')
os.system('mpiexec -n 4 python3 ../scripts/plot.py snaps/*.h5')

