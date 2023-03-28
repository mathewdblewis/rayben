print("FINISH THIS CODE")


exit()

import os; import moviepy.video.io.ImageSequenceClip
from multiprocessing import Pool

def f(s): os.system('mpiexec -n 4 python3 ../scripts/plot.py snaps/%s' % s)
os.system('cp -R snapshots snaps')
Pool(16).map(f,[snap for snap in os.listdir('snaps') if snap.endswith('.h5')])

exit()
os.system('mpiexec -n 4 python3 ../scripts/plot.py snaps/*.h5')
image_files = sorted([os.path.join('frames',img) for img in os.listdir('frames') if img.endswith(".png")])
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=10)
clip.write_videofile('movie.mov',codec="libx264")
os.system('rm -rf frames snaps')

