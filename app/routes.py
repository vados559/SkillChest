from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_session import Session
from app import db, app
from app.models import Users
from app.forms import RegisterForm

app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

users = {
    "user@example.com": "password123"
}

@app.route('/')
def main():
    Register = RegisterForm()
    if Register.validate_on_submit():
        Email, Password = Register.Email.data, Register.Password.data
        new_user = Users(Email = Email, Password = Password)
        db.session.add(new_user)
        db.session.commit()
    return render_template("main.html", user=session.get('user'), Register = Register)

@app.route('/User')
def UserProfile():
        return render_template('User.html', user=session['user'])

@app.route('/Search', methods=['GET'])
def Search():
    query = request.args.get('query')
    return f"Вы искали: {query}"

@app.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    Email = data.get('Email')
    Password = data.get('Password')
    new_user = Users(Email = Email, Password = Password)
    db.session.add(new_user)

     

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        session['user'] = email
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
