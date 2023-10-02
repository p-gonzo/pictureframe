import os

from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath('./static/pictures/library')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# Todo - pull in secret key from env config
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    pic_dir = './static/pictures/current'
    pic_path = '.' + [os.path.join(pic_dir, f) for f in os.listdir(pic_dir) if os.path.isfile(os.path.join(pic_dir, f))][0]
    return render_template('index.html', pic_path=pic_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            flash('No file part')
            return redirect(url_for('main'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            print('no selected file')
            return redirect(url_for('main'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('success')
            flash('Success')
            return redirect(url_for('main'))