from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, IntegerField, PasswordField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email

class RegisterForm(FlaskForm):
    Email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    Password = PasswordField('Пароль', validators=[DataRequired()])
    CheckPassword = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    Role = SelectField('Ваша роль', choices=[('Студент'), ('Преподаватель')], validators=[DataRequired()])
    Submit = SubmitField('Регситрация', validators=[DataRequired()])

class AuthForm(FlaskForm):
    Email = StringField('Электронная почта', validators=[DataRequired(), Length(min=1, max=128), Email()])
    Password = PasswordField('Пароль', validators=[DataRequired()])
    Submit = SubmitField('Войти')

class CourseForm(FlaskForm):
    NameCourse = StringField('Название курса', validators=[DataRequired()])
    Photo = FileField('Фото курса', validators=[DataRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    DescriptionCourse = StringField('Описание курса', validators=[DataRequired()])
    Submit = SubmitField('Добавить')

class LessonForm(FlaskForm):
    NameLesson = StringField('Название урока', validators=[DataRequired()])
    FileLesson = FileField('Материал урока', validators=[DataRequired(), FileAllowed(['mp4', 'avi', 'mov', 'mkv'], 'Video only!')])
    TextLesson = TextAreaField('Текст урока', validators=[DataRequired()], render_kw={"class": "form-control", "style": "height: 200px;"})
    Submit = SubmitField('Добавить')
