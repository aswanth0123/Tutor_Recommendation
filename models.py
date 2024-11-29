from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User model for regular users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Admin model
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    whatsapp_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    place = db.Column(db.String(100), nullable=True)
    facebook_link = db.Column(db.String(200), nullable=True)
    available_time = db.Column(db.String(100), nullable=True)
    available_days = db.Column(db.String(100), nullable=True)
    teaching_class = db.Column(db.String(50), nullable=True) 
    file_name = db.Column(db.String(200)) 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    publication = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    rack_no = db.Column(db.Integer, nullable=False)
    no_book = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200)) 
