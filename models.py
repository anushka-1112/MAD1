from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100), unique=True)
    role =  db.Column(db.String(20))
    approved = db.Column(db.Boolean(), default=False)

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(20), unique=True)
    course_code = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=True)