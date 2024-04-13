from PIL import Image
from moviepy.editor import ImageSequenceClip
import numpy as np

# Define the paths to the provided images
image1_path = './1713018610-187.40.200.149(1).jpg'
image2_path = './1713018428-187.40.200.149.jpg'

# Load images
image1 = Image.open(image1_path)
image2 = Image.open(image2_path)

# Define fps (frames per second)
fps = 20  # for a very fast flicker

# Create frame sequence with alternate images, making sure each image is one frame long
frame_sequence = [image1, image2] * (fps * 5)  # 10 seconds at 20 fps

# Create a clip from the frame sequence
clip = ImageSequenceClip([np.array(img) for img in frame_sequence], fps=fps)

# Export the clip to an mp4 file
output_file_path = 'output.mp4'
clip.write_videofile(output_file_path, codec='libx264', audio=False)

# Close the clip to release resources
clip.close()

# Provide the path to the output file
output_file_path
