import os
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

UPLOAD_FOLDER = '/home/ubuntu/wifi'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # Check if the file is allowed
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('home'))
    # Get a list of the files in the upload folder
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('home.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    # Send the file as an attachment
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
