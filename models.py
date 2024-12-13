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
    vector_data = db.Column(db.Text, nullable=True) 

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
    course = db.Column(db.String(100), nullable=False)  
    whatsapp_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    place = db.Column(db.String(100), nullable=True)
    available_time = db.Column(db.String(100), nullable=True)
    available_days = db.Column(db.String(100), nullable=True)
    teaching_class = db.Column(db.String(50), nullable=True)
    file_name = db.Column(db.String(200)) 
    duration = db.Column(db.String(100))  
    description = db.Column(db.String(500))  
    rating = db.Column(db.Float)
    vector_data = db.Column(db.Text, nullable=True) 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    publication = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    rack_no = db.Column(db.Integer, nullable=False)
    no_book = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200)) 
    file =db.Column(db.String(200))

    
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
    student_id = db.Column(db.Integer, db.ForeignKey('students.sid'), nullable=False)  # Foreign key to Student table
    demo_class_id = db.Column(db.Integer, db.ForeignKey('demo_class.id'), nullable=True)  # Foreign key to DemoClass table
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Example: 'pending', 'approved', 'rejected'
    class_link = db.Column(db.String(200),nullable=True)  # Optional class link (e.g., Zoom, Google Meet)

    # Relationships
    teacher = db.relationship('Teacher', backref='demo_requests')
    parent = db.relationship('User', backref='demo_requests')
    student = db.relationship('Student', backref='demo_requests')
    demo_class = db.relationship('DemoClass', backref='requests')


class BookBookings(db.Model):
    __tablename__ = 'book_bookings'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key to Parent (User) table
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status=db.Column(db.String(50), nullable=False)

    teacher = db.relationship('Teacher', backref='book_bookings')
    parent = db.relationship('User', backref='book_bookings')
    book = db.relationship('Book', backref='book_bookings')


class TeacherBookings(db.Model):
    __tablename__ = 'teacher_bookings'
    id = db.Column(db.Integer, primary_key=True)
    demo_class_request_id = db.Column(db.Integer, db.ForeignKey('demo_class_request.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key to Parent (User) table
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    status=db.Column(db.String(50), nullable=False)
    time=db.Column(db.String(50), nullable=True)

    teacher = db.relationship('Teacher', backref='teacher_bookings')
    parent = db.relationship('User', backref='teacher_bookings')
    demo_class_request = db.relationship('DemoClassRequest', backref='teacher_bookings')


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    rateing1 = db.Column(db.Boolean, default=False)
    rateing2 = db.Column(db.Boolean, default=False)
    rateing3 = db.Column(db.Boolean, default=False)
    rateing4 = db.Column(db.Boolean, default=False)
    rateing5 = db.Column(db.Boolean, default=False)
    comments = db.Column(db.Text, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User table
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)  # Foreign key to Teacher table

    # Relationships
    user = db.relationship('User', backref='reviews')
    teacher = db.relationship('Teacher', backref='reviews')


class search_input(db.Model):
    __tablename__ = 'search_input'
    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    # Relationships
    user = db.relationship('User', backref='search_inputs')
