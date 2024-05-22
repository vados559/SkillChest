from app import db, app
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    app.app_context().push()
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(128), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Role = db.Column(db.String(128), nullable=False)
