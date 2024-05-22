from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class RegisterForm(FlaskForm):
    Email = StringField('Электронная почта', validators=[DataRequired(), Length(min=1, max=128)])
    Password = StringField('Пароль', validators=[DataRequired()])
    CheckPassword = StringField('Подтвердите пароль', validators=[DataRequired()])
    Submit = SubmitField('Зарегестрироваться')