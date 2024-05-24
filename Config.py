import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app\\instance\\app.db')
    VIDEO_UPLOAD_FOLDER = os.path.join(basedir,'app\\static\\video')
    IMAGE_UPLOAD_FOLDER = os.path.join(basedir,'app\\static\\image')
    SQLALCHEMY_TRACK_MODIFICATIONS = False