from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@127.0.0.1/url_shortener'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "<enter your secret key>"
db = SQLAlchemy(app)

from Models import ShortUrl

@app.route("/")
def home():
    return render_template('short_url.html')

@app.route("/shorten/url/", methods = ['GET', 'POST'])
def shorten_url():
    if request.method == 'GET':
        return render_template('short_url.html')
    elif not request.form['url']:
        message = "Please enter url"
        return render_template('short_url.html', message = message)
    else:
        # Assumption here is that only a valid url is being submitted and is shorter than 355 characters
        request_url = request.form['url']
        short_url = get_shortened_url(request_url)
        # If a repeated url is being passed, then we re-use the shortened version of the url instead of creating a new one
        if short_url:
            return render_template('short_url.html', short_url = short_url)
        # A moving 8-character window is used to generate a hash for the short version of url
        new_short_url = generate_short_url(request_url)
        if new_short_url:
            short_url = ShortUrl.ShortUrl(url = request_url, short_url = new_short_url)
            db.session.add(short_url)
            db.session.commit()
            return render_template('short_url.html', short_url = short_url)
        else:
            message = "Sorry! Can't shorten this url"
            return render_template('short_url.html', message = message)

@app.route("/all/")
def show_all():
    return render_template('show_all.html', urls = ShortUrl.ShortUrl.query.all())

@app.route("/original/url/",methods = ['GET', 'POST'])
def original_url():
    if request.method == 'GET':
        return render_template('original_url.html')
    elif not request.form['short_url']:
        message = "Please enter a short url"
        return render_template('original_url.html', message = message)
    else:
        short_url = request.form['short_url'].split("/")
        if len(short_url) != 4:
            message = "Please enter a valid short url"
            return render_template('original_url.html', message = message)
        short_url = ShortUrl.ShortUrl.query.filter_by(short_url = short_url[3]).first()
        if short_url:
            return render_template('original_url.html', result = short_url)
        else:
            message = "Invalid short url provided"
            return render_template('original_url.html', message = message)

def get_shortened_url(url):
    return ShortUrl.ShortUrl.query.filter_by(url = url).first()

def is_short_url_in_use(short_url):
    if ShortUrl.ShortUrl.query.filter_by(short_url = short_url).first():
        return True
    else:
        return False

# This function generates a new hash for every requested url. In case there is an overlap of the 8 characters that are used to for hash,
# making use of a moving 8-character window so that we always generate a new hash for a new url. The system, however, does not
# support an alternate approach to handle duplicate hashes
def generate_short_url(url):
    short_url = hashlib.md5(url.encode())
    string_start = 0
    string_end = 8
    counter = 0
    while(counter < 24):
        short_url_considered = short_url.hexdigest()[(string_start + counter) : (string_end + counter)]
        if is_short_url_in_use(short_url = short_url_considered):
            counter+= 1
        else:
            return short_url_considered
    if counter == 24:
        return False
