from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from flask_session import Session
from app import db, app
from app.models import Users, Courses, Lessons
from app.forms import RegisterForm, AuthForm, CourseForm, LessonForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
from pathlib import Path

app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def main():
    Register = RegisterForm()
    Auth = AuthForm()
    reg_message = None
    auth_message = None
    reg_success = False

    if Register.validate_on_submit() and request.form['form-name'] == 'register-form':
        Email, Password, Role = Register.Email.data, Register.Password.data, Register.Role.data

        if Register.Password.data != Register.CheckPassword.data:
            reg_message = "Пароли не совпадают"
        else:
            new_user = Users(Email=Email, Password=Password, Role = Role)
            db.session.add(new_user)
            db.session.commit()
            reg_message = "Вы успешно зарегистрированы"
            reg_success = True

    if Auth.validate_on_submit() and request.form['form-name'] == 'auth-form':
        Email, Password = Auth.Email.data, Auth.Password.data
        user = Users.query.filter_by(Email=Email).first()
        if user and user.Password == Password:
            login_user(user)
            return redirect(url_for('main'))
        else:
            auth_message = "Логин или почта не верны"

    return render_template('main.html', 
                           Register = Register, 
                           Auth = Auth, 
                           reg_message = reg_message, 
                           reg_success = reg_success, 
                           auth_message = auth_message)


@app.route('/User')
@login_required
def UserProfile():
        return render_template('User.html', 
                               UserEmail=current_user.Email,
                               UserRole = current_user.Role,
                               UserId = current_user.id)

@app.route('/AddCourse', methods = ['GET', 'POST'])
def AddCourse():
    FormCourse = CourseForm()
    if FormCourse.validate_on_submit() and request.form['form-name'] == 'course-form':
        Name, PhotoName, Desc = FormCourse.NameCourse.data, secure_filename(FormCourse.Photo.data.filename), FormCourse.DescriptionCourse.data
        new_course = Courses(Author_id = current_user.id, 
                             Name_Course = Name, 
                             Photo_Path = "image" + "/" + str(current_user.id) + "/" + PhotoName, 
                             Description = Desc)
        db.session.add(new_course)
        db.session.commit()
        directory = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], str(current_user.id))
        if not os.path.isdir(directory):
            os.mkdir(directory)        
        FormCourse.Photo.data.save(os.path.join(directory, PhotoName))
        return redirect(url_for('main'))
    user_courses = Courses.query.filter_by(Author_id=current_user.id).all()
    return render_template("AddCourse.html", Form=FormCourse, user_courses=user_courses)

@app.route("/CourseDetail/<int:CourseId>")
def CourseDetail(CourseId: int):
    course = Courses.query.filter_by(id=CourseId).first()
    if course is None:
        return redirect(url_for('main'))  # Или отобразить страницу 404
    AllLessons = Lessons.query.filter_by(Course_id = CourseId).all()
    return render_template("CourseDetail.html", course=course, AllLessons = AllLessons)

@app.route("/AddLesson/<int:CourseId>", methods=['GET', 'POST'])
def AddLesson(CourseId: int):
    FormLesson = LessonForm()
    if FormLesson.validate_on_submit() and request.form['form-name'] == 'lesson-form':
        Title, MaterialName, Text = FormLesson.NameLesson.data, secure_filename(FormLesson.FileLesson.data.filename), FormLesson.TextLesson.data
        new_lesson = Lessons(Course_id = CourseId, 
                             Name_Lesson = Title, 
                             Material_Path = "video" + "/" + str(current_user.id) + "/" + MaterialName,
                             Text = Text)
        db.session.add(new_lesson)
        db.session.commit()
        directory = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], str(current_user.id))
        if not os.path.isdir(directory):
            os.mkdir(directory)        
        FormLesson.FileLesson.data.save(os.path.join(directory, MaterialName))
        return redirect(url_for("CourseDetail", CourseId = CourseId))
    return render_template("AddLesson.html", Form = FormLesson)

    

@app.route("/AllCourses")
def AllCourses():
    All_Courses = Courses.query.all()
    return render_template("AllCourses.html", Courses = All_Courses)

@app.route('/Search', methods=['GET'])
def Search():
    query = request.args.get('query')
    print(query)
    if query == "":
        return redirect(url_for('main'))
    else:
        return f"Вы искали: {query}"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))
