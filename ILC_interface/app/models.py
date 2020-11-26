from . import db 

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.STring(100), unique=True)
    password = db.Column(db.String(100))