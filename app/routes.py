from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from flask_session import Session
from app import db, app
from app.models import Users
from app.forms import RegisterForm, AuthForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

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
        Email, Password = Register.Email.data, Register.Password.data

        if Register.Password.data != Register.CheckPassword.data:
            reg_message = "Пароли не совпадают"
        else:
            new_user = Users(Email=Email, Password=Password)
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
