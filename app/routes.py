from flask import render_template, redirect, url_for, request, flash
from app import db, app
from app.models import Users, Courses, Lessons
from app.forms import RegisterForm, AuthForm, CourseForm, LessonForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
from sqlalchemy import or_

app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager(app)
login_manager.login_view = 'main'

def Registration(Reg):
    reg_message = None
    reg_success = False

    Email, Password, Role = Reg.Email.data, Reg.Password.data, Reg.Role.data

    if Reg.Password.data != Reg.CheckPassword.data:
        reg_message = "Пароли не совпадают"
    else:
        new_user = Users(Email=Email, Password=Password, Role = Role)
        db.session.add(new_user)
        db.session.commit()
        reg_message = "Вы успешно зарегистрированы"
        reg_success = True
    return reg_message, reg_success
        
def Login(Auth):
    auth_message = None
    Email, Password = Auth.Email.data, Auth.Password.data
    user = Users.query.filter_by(Email=Email).first()
    if user and user.Password == Password:
        login_user(user)
        return None
    else:
        auth_message = "Логин или почта не верны"
        return auth_message

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
       reg_message, reg_success = Registration(Register)

    if Auth.validate_on_submit() and request.form['form-name'] == 'auth-form':
        auth_message = Login(Auth)

    return render_template('main.html', 
                           Register = Register, 
                           Auth = Auth, 
                           reg_message = reg_message, 
                           reg_success = reg_success, 
                           auth_message = auth_message)


@app.route('/User')
@login_required
def UserProfile():
        user_courses = Courses.query.filter(Courses.id.in_(current_user.Course_List)).all()
        return render_template('User.html', 
                               UserEmail=current_user.Email,
                               UserRole = current_user.Role,
                               UserId = current_user.id,
                               user_courses = user_courses)

@app.route('/AddCourse', methods = ['GET', 'POST'])
@login_required
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

@app.route("/CourseDetail/<int:CourseId>", methods=['GET', 'POST'])
def CourseDetail(CourseId: int):
    Register = RegisterForm()
    Auth = AuthForm()
    reg_message = None
    auth_message = None
    reg_success = False

    if Register.validate_on_submit() and request.form['form-name'] == 'register-form':
       reg_message, reg_success = Registration(Register)

    if Auth.validate_on_submit() and request.form['form-name'] == 'auth-form':
        auth_message = Login(Auth)

    course = Courses.query.filter_by(id=CourseId).first()
    if course is None:
        return redirect(url_for('main'))  # Или отобразить страницу 404
    AllLessons = Lessons.query.filter_by(Course_id = CourseId).all()
    return render_template("CourseDetail.html", 
                           course=course, 
                           AllLessons = AllLessons,
                           Register = Register, 
                           Auth = Auth, 
                           reg_message = reg_message, 
                           reg_success = reg_success, 
                           auth_message = auth_message)

@app.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    user = Users.query.get_or_404(current_user.id)
    course_list = user.Course_List  # Извлекаем десериализованный список
    
    if str(course_id) not in course_list:
        course_list.append(str(course_id))  # Преобразуем course_id в строку
        user.Course_List = course_list  # Обновляем сериализованный список в базе данных
        db.session.commit()
        flash('Вы успешно записались на курс!', 'success')
    
    return redirect(url_for('CourseDetail', CourseId=course_id))


@app.route("/AddLesson/<int:CourseId>", methods=['GET', 'POST'])
@login_required
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

    

@app.route("/AllCourses", methods = ['GET', 'POST'])
def AllCourses():
    Register = RegisterForm()
    Auth = AuthForm()
    reg_message = None
    auth_message = None
    reg_success = False

    if Register.validate_on_submit() and request.form['form-name'] == 'register-form':
       reg_message, reg_success = Registration(Register)

    if Auth.validate_on_submit() and request.form['form-name'] == 'auth-form':
        auth_message = Login(Auth)
         
    All_Courses = Courses.query.all()
    return render_template("AllCourses.html", 
                           Courses = All_Courses,
                           Register = Register, 
                           Auth = Auth, 
                           reg_message = reg_message, 
                           reg_success = reg_success, 
                           auth_message = auth_message)

@app.route('/Search', methods = ['GET', 'POST'])
def Search():
    Register = RegisterForm()
    Auth = AuthForm()
    reg_message = None
    auth_message = None
    reg_success = False

    if Register.validate_on_submit() and request.form['form-name'] == 'register-form':
       reg_message, reg_success = Registration(Register)

    if Auth.validate_on_submit() and request.form['form-name'] == 'auth-form':
        auth_message = Login(Auth)
    
    query = request.args.get('query')
    if query == "":
        return redirect(url_for('main'))
    elif query:
        search_pattern = f"%{query}%"
        results = Courses.query.filter(
            or_(
                Courses.Name_Course.like(search_pattern),
                Courses.Description.like(search_pattern)
            )
        ).all()
    else:
        results = []
    return render_template("SearchResults.html", 
                           results=results, 
                           query=query,
                           Register = Register, 
                           Auth = Auth, 
                           reg_message = reg_message, 
                           reg_success = reg_success, 
                           auth_message = auth_message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))
