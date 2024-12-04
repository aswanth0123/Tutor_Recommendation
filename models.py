from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User model for regular users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
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

    
class Student(db.Model):
    __tablename__ = 'students'  # Table name
    sid = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(25), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    clad = db.Column(db.String(30), nullable=False)
    img = db.Column(db.String(50), nullable=False)
    parent = db.relationship('User', backref='students')

class DemoClass(db.Model):
    __tablename__ = 'demo_class'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    subject = db.Column(db.String(100), nullable=False)
    class_details = db.Column(db.String(200), nullable=False)
    video = db.Column(db.String(200), nullable=False)  # URL or path to video file
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)  # Foreign key to Teacher table
    date = db.Column(db.Date, nullable=False)

    # Relationship with the Teacher model
    teacher = db.relationship('Teacher', backref='demo_classes')

class DemoClassRequest(db.Model):
    __tablename__ = 'demo_class_request'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)  # Foreign key to Teacher table
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to Parent (User) table
    student_id = db.Column(db.Integer, db.ForeignKey('student.sid'), nullable=False)  # Foreign key to Student table
    demo_class_id = db.Column(db.Integer, db.ForeignKey('demo_class.id'), nullable=False)  # Foreign key to DemoClass table
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Example: 'pending', 'approved', 'rejected'
    class_link = db.Column(db.String(200))  # Optional class link (e.g., Zoom, Google Meet)

    # Relationships
    teacher = db.relationship('Teacher', backref='demo_requests')
    parent = db.relationship('User', backref='demo_requests')
    student = db.relationship('students', backref='demo_requests')
    demo_class = db.relationship('DemoClass', backref='requests')