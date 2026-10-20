from flask import Flask, redirect, render_template, request, url_for
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///exam_mgmnt.db'
db.init_app(app)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role='admin').first()
    if admin is None:
        admin = User(user_name = 'Admin',
                     role= 'admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return render_template("home.html")

if __name__=="__main__":
    app.run()