from flask import Flask, request, send_file, render_template
from PIL import Image
from moviepy.editor import ImageSequenceClip
import numpy as np
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_PATH'] = 10000000  # Adjust as needed

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image1' not in request.files or 'image2' not in request.files:
            return 'No file part'

        image1 = request.files['image1']
        image2 = request.files['image2']
        fps = int(request.form.get('fps', 20))
        duration = int(request.form.get('duration', 5))
        output_format = request.form.get('format', 'mp4')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image1.filename == '' or image2.filename == '':
            return 'No selected file'

        if image1 and image2:
            filename1 = secure_filename(image1.filename)
            filename2 = secure_filename(image2.filename)
            image1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            image2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            image1.save(image1_path)
            image2.save(image2_path)

            # Process images
            output_file_path = process_images(image1_path, image2_path, fps, duration, output_format)
            
            # Send file
            return send_file(output_file_path, as_attachment=True)

    # GET request returns the upload form
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      Image 1: <input type=file name=image1>
      Image 2: <input type=file name=image2>
      FPS: <input type=number name=fps value=20>
      Duration (sec): <input type=number name=duration value=5>
      Output format: <select name=format>
                        <option value="mp4">MP4</option>
                        <option value="gif">GIF</option>
                     </select>
      <input type=submit value=Run>
    </form>
    '''

def process_images(image1_path, image2_path, fps, duration, output_format):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    frame_sequence = [image1, image2] * (fps * duration)
    clip = ImageSequenceClip([np.array(img) for img in frame_sequence], fps=fps)

    if output_format == 'mp4':
        output_file_path = './output.mp4'
        clip.write_videofile(output_file_path, codec='libx264', audio=False)
    elif output_format == 'gif':
        output_file_path = './output.gif'
        clip.write_gif(output_file_path, fps=fps)

    clip.close()
    return output_file_path

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
