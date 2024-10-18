import os
from flask import Flask, render_template, request, send_from_directory
from kmeans_compression import compress_image
from PIL import Image

app = Flask(__name__)

CLUSTERS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# Folder to store uploaded and compressed images
UPLOAD_FOLDER = 'static/compressed_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the file is present
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            _, extension = os.path.splitext(file.filename)
            filename = 'original_image' + extension
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Compress image using k-means
            clusters = int(request.form['clusters'])
            compressed_img = compress_image(filepath, clusters)

            # Save compressed image
            compressed_filename = 'compressed_image' + extension
            compressed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)
            Image.fromarray(compressed_img).save(compressed_filepath)

        

            return render_template('index.html',
                                   original_image=filename,
                                   compressed_image=compressed_filename,clusters = CLUSTERS)

    return render_template('index.html',clusters = CLUSTERS)

@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
