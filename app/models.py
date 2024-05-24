from app import db, app
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    app.app_context().push()
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(128), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Role = db.Column(db.String(128), nullable=False)
    CourseList = db.Column(db.Integer)

class Courses(db.Model):
    app.app_context().push()
    id = db.Column(db.Integer, primary_key=True)
    Author_id = db.Column(db.Integer, nullable=False)
    Name_Course = db.Column(db.String(128), nullable=False)
    Photo_Path = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)

class Lessons(db.Model):
    app.app_context().push()
    id = db.Column(db.Integer, primary_key=True)
    Course_id = db.Column(db.Integer, nullable=False)
    Name_Lesson = db.Column(db.String(128), nullable=False)
    Material_Path = db.Column(db.String, nullable=False)
    Text = db.Column(db.String)



