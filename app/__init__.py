from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from Config import Config
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
# app.config['SECRET_KEY'] = 'vad748'
# csrf = CSRFProtect(app)

db = SQLAlchemy(app)

from app import routes, models
with app.app_context():
    db.create_all()
