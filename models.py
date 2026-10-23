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

class Examination(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(20), unique=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    exam_type = db.Column(db.String(20))
    duration = db.Column(db.String(20))
    max_marks = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
#exam= Examination.query.filter_by(user_id=examiner_id).all()
class Timeline(db.Model):
    timeline_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('examination.exam_id'), unique=True)
    slot_start = db.Column(db.String(20))
    slot_end = db.Column(db.String(20))
    booking_deadline = db.Column(db.String(20))
    slot_open = db.Column(db.Boolean(), default=False)
    booking_open = db.Column(db.Boolean(), default=False)

class Slot(db.Model):
    slot_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('examination.exam_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    slot_date = db.Column(db.String(20))
    slot_time = db.Column(db.String(20))


#user_id ->examiner = Examination(assign), ExaminationRubrics(exam evaluation)

#user -> studnet = Slot(to give exam)