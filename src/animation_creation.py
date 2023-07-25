import imageio
import os
# List all files in the directory with the .png extension
image_files = sorted([f for f in os.listdir() if f.endswith('.png')])

# Read each file into an array
images = [imageio.imread(f) for f in image_files]
# Save the images as an animation
imageio.mimsave('animation2.mp4', images, fps=30)