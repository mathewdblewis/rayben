import moviepy.video.io.ImageSequenceClip
import os

image_files = sorted([os.path.join('frames',img) for img in os.listdir('frames') if img.endswith(".png")])
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=10)
clip.write_videofile('movie.mov',codec="libx264")

