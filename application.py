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
def photos():
    pics_dir = './static/pictures/library'
    pics_path = ['.' + os.path.join(pics_dir, f) for f in os.listdir(pics_dir) if os.path.isfile(os.path.join(pics_dir, f))]
    return render_template('photos.html', photos=pics_path)

@app.route('/crop/<idx>', methods=['POST', 'GET'])
def crop(idx=None):
    if request.method == 'GET':
        pics_dir = './static/pictures/library'
        pics_path = ['.' + os.path.join(pics_dir, f) for f in os.listdir(pics_dir) if os.path.isfile(os.path.join(pics_dir, f))]
        photo = pics_path[int(idx)]
        return render_template('crop.html', photo=photo)
    elif request.method == 'POST':
        return

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "", 403
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return "", 403
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pics_dir = './static/pictures/library'
            pics_names = [f for f in os.listdir(pics_dir) if os.path.isfile(os.path.join(pics_dir, f))]
            print(pics_names.index(filename))
            print(pics_names)
            return redirect(f'/crop/{str(pics_names.index(filename))}')
    elif request.method == 'GET':
        return render_template('upload.html')