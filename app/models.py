from app import db, app

class Users(db.Model):
    app.app_context().push()
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(128), nullable=True)
    Password = db.Column(db.String(128), nullable=True)
    Name = db.Column(db.String(128), nullable=False)