import os
from subprocess import Popen, call

from flask import Flask, render_template, request, redirect
from PIL import Image
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath('./static/pictures/library')
COMPRESSED_FOLDER = os.path.abspath('./static/pictures/compressed')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# Todo - pull in secret key from env config
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

@app.route('/photos')
def photos():
    pics_dir = './static/pictures/library'
    compressed_dir = './static/pictures/compressed'
    pics_path = ['.' + os.path.join(pics_dir, f) for f in os.listdir(pics_dir) if os.path.isfile(os.path.join(pics_dir, f))]
    compressed_path = ['.' + os.path.join(compressed_dir, f) for f in os.listdir(compressed_dir) if os.path.isfile(os.path.join(compressed_dir, f))]
    return render_template('photos.html', photos=zip(pics_path, compressed_path))

@app.route('/')
def current():
    photo = './static/pictures/current/image.jpg'
    return render_template('current.html', photo=photo)

@app.route('/crop/<idx>')
def crop(idx=None):
    pics_dir = './static/pictures/library'
    pics_path = ['.' + os.path.join(pics_dir, f) for f in os.listdir(pics_dir) if os.path.isfile(os.path.join(pics_dir, f))]
    photo = pics_path[int(idx)]
    return render_template('crop.html', photo=photo)

@app.route('/crop', methods=['POST'])
def crop_photo():
    image_path = request.form['image'][1:]
    x = float(request.form['x'])
    y = float(request.form['y'])
    w = float(request.form['width'])
    h = float(request.form['height'])
    r = float(request.form['rotate'])
    with Image.open(image_path) as im:
        # The crop method from the Image module takes four coordinates as input.
        # The right can also be represented as (left+width)
        # and lower can be represented as (upper+height)
        im_rot = im.rotate(angle=r*-1, expand=1)
        im_crop = im_rot.crop((x, y, x + w, y + h))
        im_resized = im_crop.resize((600,448))
        im_resized.save('./static/pictures/current/image.jpg')
        
        p = Popen("python3 /home/phil/Pimoroni/inky/examples/7color/image.py /home/phil/pictureframe/static/pictures/current/image.jpg", shell=True)

    return redirect('/')

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
            save_compressed_image(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(f'/crop/{str(pics_names.index(filename))}')
    elif request.method == 'GET':
        return render_template('upload.html')
    
@app.route('/delete', methods =['POST'])
def delete():
   image_path = request.form['image'][1:]
   call(f"rm {os.path.abspath(image_path)}", shell=True)
   return redirect('/photos')

if __name__ == '__main__':
    app.run()

def save_compressed_image(file_path, img_name):
    
    base_width= 600
    img = Image.open(file_path)
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    # TODO - Add logic to toggle between both of these based on Python Version
    # img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img = img.resize((base_width, hsize), Image.LANCZOS)
    img.save(os.path.join(app.config['COMPRESSED_FOLDER'], img_name))
