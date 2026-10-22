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
                return redirect(url_for("studentdashboard", user_details=user.user_name))
            if user.role == 'examiner' and user.approved:
                return redirect(url_for("examinerdashboard", user_details=user.user_name))
    return render_template("login.html")

@app.route('/admin_dashboard/<user_details>')
def admin_dashboard(user_details):
    user = User.query.filter_by(user_name = user_details).first()
    courses = Courses.query.all()
    users = User.query.all()
    exams = Examination.query.all()
    return render_template("admindashboard.html", user = user, courses=courses, users = users,
                           exams= exams)

@app.route('/studentdashboard/<user_details>')
def studentdashboard(user_details):
    user = User.query.filter_by(user_name = user_details).first()
    return render_template("studentdashboard.html", user = user)

@app.route('/examinerdashboard/<user_details>')
def examinerdashboard(user_details):
    user = User.query.filter_by(user_name = user_details).first()
    return render_template("examinerdashboard.html", user = user)

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

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method=='POST':
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")
        role = request.form.get("role")
        user = User(user_name=user_name,
                    password=user_password,
                    role=role)
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    return render_template("register.html")

@app.route('/approve/<user_id>/<admin_details>', methods=['GET', 'POST'])
def approve(user_id, admin_details):
    user = User.query.filter_by(user_id=user_id).update(dict(approved=True))
    db.session.commit()
    return redirect(url_for("admin_dashboard", user_details=admin_details))

@app.route('/search', methods=['POST'])
def search():
    admin_details = User.query.filter_by(role='admin').first()
    searched_string = request.form.get('searched_string', '').strip()
    all_users = []
    all_examinations = []
    all_bookings = []
    if searched_string:
        users_by_name = User.query.filter(User.user_name.ilike(f'%{searched_string}%')).all()
        users_by_id = User.query.filter(User.user_id.ilike(f'%{searched_string}%')).all()
        all_users=users_by_id+users_by_name
        return render_template('searched_results.html', users = all_users)
    return redirect(url_for("admin_dashboard", user_details=admin_details.user_name))


@app.route('/add_exam/<user_details>', methods=['GET', 'POST'])
def add_exam(user_details):
    user = User.query.filter_by(user_name = user_details).first()
    courses = Courses.query.all()
    if request.method=='POST':
        user = User.query.filter_by(user_name = user_details).first()
        exam_name = request.form.get('exam_name')
        exam_type = request.form.get('exam_type')
        duration = request.form.get('duration')
        max_marks = request.form.get('max_marks')
        course_id = request.form.get('course_id')
        exam = Examination(exam_name=exam_name,
                           exam_type = exam_type,
                           course_id = course_id,
                           duration = duration,
                           max_marks = max_marks)
        db.session.add(exam)
        db.session.commit()
        return redirect(url_for("admin_dashboard", user_details=user.user_name))
    return render_template('add_exam.html', user = user, courses=courses)

@app.route('/assign/<exam_id>', methods=['GET', 'POST'])
def assign_exam(exam_id):
    examiners = User.query.filter_by(role='examiner').all()
    if request.method=='POST':
        examiner_id = request.form.get('examiner_id')
        exam = Examination.query.filter_by(exam_id = exam_id).update(dict(user_id = examiner_id))
        db.session.commit()
        return redirect(url_for("admin_dashboard", user_details='Admin'))
    return render_template('assign.html', examiners = examiners, exam_id=exam_id)

if __name__=="__main__":
    app.run()