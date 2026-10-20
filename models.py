from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)
    role =  db.Column(db.String(20))