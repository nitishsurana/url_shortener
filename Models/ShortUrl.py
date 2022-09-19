from app import db

class ShortUrl(db.Model):
    short_url_id = db.Column('short_url_id', db.Integer, primary_key = True)
    url = db.Column(db.String(355),nullable = False)
    short_url = db.Column(db.String(10),nullable = False)

def __init__(self, url, short_url):
    self.url = url
    self.short_url = short_url

def __repr__(self):
    return f'<ShortUrl {self.url}>'
