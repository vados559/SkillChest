from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email

class RegisterForm(FlaskForm):
    Email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    Password = PasswordField('Пароль', validators=[DataRequired()])
    CheckPassword = PasswordField('Подтвердите Password', validators=[DataRequired()])
    Role = SelectField('Ваша роль', choices=[('Студент'), ('Преподаватель')], validators=[DataRequired()])
    Submit = SubmitField('Register', validators=[DataRequired()])

class AuthForm(FlaskForm):
    Email = StringField('Электронная почта', validators=[DataRequired(), Length(min=1, max=128), Email()])
    Password = PasswordField('Пароль', validators=[DataRequired()])
    Submit = SubmitField('Войти')