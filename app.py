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
                     password = 'admin123',
                     role= 'admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")
        user = User.query.filter_by(user_name=user_name).first()
        if user and user.password == user_password:
            if user.role == 'admin':
                return redirect(url_for("admin_dashboard", user_details=user.user_name))
            if user.role == 'student':
                return redirect("studentdashboard")
            if user.role == 'examiner' and user.approved:
                return redirect("examinerdashboard")
    return render_template("login.html")

@app.route('/admin_dashboard/<user_details>')
def admin_dashboard(user_details):
    user = User.query.filter_by(user_name = user_details).first()
    courses = Courses.query.all()
    return render_template("admindashboard.html", user = user, courses=courses)

@app.route('/add_course/<user_details>', methods=['GET', 'POST'])
def add_course(user_details):
    user = User.query.filter_by(user_name = user_details).first()
    if request.method=='POST':
        user = User.query.filter_by(user_name = user_details).first()
        course_name = request.form.get('course_name')
        course_code = request.form.get('course_code')
        description = request.form.get('description')
        course = Courses(course_name= course_name,
                         course_code = course_code,
                         description = description)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for("admin_dashboard", user_details=user.user_name))
    return render_template('add_course.html', user = user)

@app.route('/edit_courses/<user_details>/<course_id>', methods=['GET', 'POST'])
def edit_courses(user_details, course_id):
    user = User.query.filter_by(user_name = user_details).first()
    course = Courses.query.filter_by(course_id=course_id).first()
    if request.method=='POST':
        course_name = request.form.get('course_name')
        course_code = request.form.get('course_code')
        description = request.form.get('description')
        course = Courses.query.filter_by(course_id=course_id).update(dict(
            course_name=course_name,
            course_code=course_code,
            description=description
        ))
        db.session.commit()
        return redirect(url_for("admin_dashboard", user_details=user.user_name))
    return render_template('edit_courses.html', user = user, course=course)

@app.route('/delete_courses/<course_id>/<user_name>')
def delete_course(course_id, user_name):
    course = Courses.query.filter_by(course_id=course_id).delete()
    db.session.commit()
    return redirect(url_for("admin_dashboard", user_details=user_name))


if __name__=="__main__":
    app.run()