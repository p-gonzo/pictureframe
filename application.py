import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/')
def main():
    pic_dir = './static/pictures/current'
    pic_path = '.' + [os.path.join(pic_dir, f) for f in os.listdir(pic_dir) if os.path.isfile(os.path.join(pic_dir, f))][0]
    print(pic_path)
    return render_template('index.html', pic_path=pic_path)