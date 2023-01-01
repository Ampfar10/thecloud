import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory 

app = Flask(__name__)

UPLOAD_FOLDER = '/home/ubuntu/wifi/upload'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() #in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.form.get('search')
    if search_query:
        # Filter the list of files based on the search query
        files = [f for f in os.listdir(UPLOAD_FOLDER) if search_query in f]
    else:
        # Get a list of all the files in the upload folder
        files = os.listdir(UPLOAD_FOLDER)

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

    return render_template('home.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    # Get a list of the files uploaded
    uploaded_files = request.files.getlist("file")

    # Loop through the uploaded files
    for uploaded_file in uploaded_files:
            # Save the file to the server
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
    # Redirect the user to the uploaded files page
    return redirect(url_for('uploaded_files'))

@app.route('/download/<filename>')
def download(filename):
    # Send the file as an attachment
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2345)
