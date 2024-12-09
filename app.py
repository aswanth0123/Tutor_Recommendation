from flask import Flask, render_template, redirect, url_for, flash, request,session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import *  # Import models from models.py
import os
from werkzeug.utils import secure_filename
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '43e77e90e26e1ddee83ea02b35065b805630944d4bd13d3abcbd120627d308a9' # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Project:Project123@localhost/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/uploads/'  # Directory to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Initialize extensions
db.init_app(app)  # Bind db to the Flask app
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    return admin if admin else User.query.get(int(user_id))

# Routes (Admin login, dashboard, logout, etc.)
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        print(admin)
        if admin and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('admin_side/login.html')

@app.route('/admin_dashboard')
# @login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash("Access denied.", "danger")
        return redirect(url_for('admin_login'))
    return render_template('admin_side/index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phno']
        email = request.form['email']
        subject = request.form['subject']
        whatsapp_number = request.form['whatsapp_number']
        address = request.form['address']
        place = request.form['place']
        facebook_link = request.form['facebook_link']
        available_time = request.form['available_time']
        available_days = request.form['available_days']
        teaching_class = request.form['teaching_class']

        file = request.files['file']


        # Create and save new teacher instance
        try:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('No file uploaded.', 'danger')
                return redirect(request.url)
            new_teacher = Teacher(
                name=name,
                phone_number=phone_number,
                email=email,
                subject=subject,
                whatsapp_number=whatsapp_number,
                address=address,
                place=place,
                facebook_link=facebook_link,
                available_time=available_time,
                available_days=available_days,
                teaching_class=teaching_class,
                file_name=filename  # Save the file name/path in the database
            )

            db.session.add(new_teacher)
            db.session.commit()
        except:
            return "<script>alert('Teacher details already exists!');window.location='/add_teacher';</script>"

        flash('Teacher registered successfully!', 'success')
        return redirect(url_for('add_teacher'))
    return render_template('admin_side/add_teacher.html')

@app.route('/admin_view_teacher')
@login_required
def admin_display_teacher():
    data=Teacher.query.all()
    return render_template('admin_side/view_teacher.html',data=data)

@app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)

    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.phone_number = request.form['phno']
        teacher.email = request.form['email']
        teacher.subject = request.form['subject']
        teacher.whatsapp_number = request.form['whatsapp_number']
        teacher.address = request.form['address']
        teacher.place = request.form['place']
        teacher.facebook_link = request.form['facebook_link']
        teacher.available_time = request.form['available_time']
        teacher.available_days = request.form['available_days']
        teacher.teaching_class = request.form['teaching_class']
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:  # Check if a file was uploaded
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # Update file name in the database
                teacher.file_name = filename
        
        # Save the updated data to the database
        db.session.commit()
        flash('Teacher details updated successfully!', 'success')
        return redirect(url_for('edit_teacher', teacher_id=teacher_id))
    return render_template('admin_side/edit_teacher.html',teacher=teacher)

@app.route('/delete_teacher/<int:teacher_id>')
@login_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('admin_display_teacher'))

@app.route('/add_book',methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book_name = request.form['b_name']
        author = request.form['author']
        publication = request.form['publication']
        subject = request.form['subject']
        rack_no = request.form['rack_no']
        no_book = request.form['no_book']
        
        # Handle file upload
        image_file = request.files['file']
        image_filename = None
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        # Create new book instance and add to database
        new_book = Book(
            book_name=book_name,
            author=author,
            publication=publication,
            subject=subject,
            rack_no=int(rack_no),
            no_book=int(no_book),
            image=image_filename
        )
        
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('admin_view_books')) 
    return render_template('admin_side/add_book.html')

@app.route('/admin_view_books')
@login_required
def admin_view_books():
    books = Book.query.all()
    return render_template('admin_side/view_book.html', books=books)


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.book_name = request.form['b_name']
        book.author = request.form['author']
        book.publication = request.form['publication']
        book.subject = request.form['subject']
        book.rack_no = request.form['rack_no']
        book.no_book = request.form['no_book']

        # Handle file upload
        image_file = request.files['file']
        image_filename = None
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            book.image = image_filename

        db.session.commit()
        flash('Book details updated successfully!', 'success')
        return redirect(url_for('edit_book', book_id=book_id))

    return render_template('admin_side/edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):    
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)    
    db.session.commit()    
    flash('Book deleted successfully!', 'success')    
    return redirect(url_for('admin_view_books'))

@login_required
@app.route('/view_parent')
def view_parent():
    parents = User.query.all()
    return render_template('admin_side/view_parents.html', parents=parents)


@login_required 
@app.route('/view_demo_class')
def view_demo_class():
    demo_class = DemoClass.query.all()
    return render_template('admin_side/view_demo_class.html', Demo_class=demo_class)


@login_required
@app.route('/view_book_requests')
def view_book_requests():
    book_requests = BookBookings.query.all()
    return render_template('admin_side/book_request.html', book_requests=book_requests)


@login_required
@app.route('/accept_book_request/<int:request_id>')
def accept_book_request(request_id):
    request = BookBookings.query.get_or_404(request_id)
    request.status = 'accepted'
    db.session.commit()
    flash('Book request accepted successfully!', 'success')
    return redirect(url_for('view_book_requests'))

@login_required
@app.route('/reject_book_request/<int:request_id>')
def reject_book_request(request_id):
    request = BookBookings.query.get_or_404(request_id)
    request.status = 'rejected'
    db.session.commit()
    flash('Book request rejected successfully!', 'success')
    return redirect(url_for('view_book_requests'))


#------------------------------parent--------------------------------------

@app.route('/', methods=['GET', 'POST'])
def parent_teacher_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']
        
        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()   
        teacher=Teacher.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Store user data in the session
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('parent_dashboard'))  # Redirect to a protected route
        elif teacher:
            # Store user data in the session
            session['teacher_id'] = teacher.id
            session['teaher_name'] = teacher.name
            flash('Login successful!', 'success')
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return "<script>alert('Invalid email or password');window.location='/';</script>"
    
    return render_template('login.html')

@app.route('/parent_teacher_logout')
def parent_teacher_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('parent_teacher_login'))

@app.route('/parent_dashboard')
def parent_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('parent_teacher_login'))
    teacher=Teacher.query.all()
    student=Student.query.filter_by(parent_id=session['user_id']).all()
    books=Book.query.all()
    accepted_books=BookBookings.query.filter_by(parent_id=session['user_id'],status='accepted').all()
    print(accepted_books)
    return render_template('parent_side/index.html',teachers=teacher,students=student,books=books,accepted_books=accepted_books)



@app.route('/parent_register', methods=['GET', 'POST'])
def parent_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phno']
        address = request.form['address']
        password = bcrypt.generate_password_hash(request.form['pwd'])  # Hashing the password for security
        
        # Create new user instance
        try:
            new_user = User(
                name=name,
                email=email,
                phone_number=phone_number,
                address=address,
                password=password
            )
            
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
        except:
            return "<script>alert('Email already exists');window.location='/';</script>"
        return redirect(url_for('parent_teacher_login'))

@app.route('/add_std', methods=['GET', 'POST'])
def add_std():
    if request.method == 'POST':
        name = request.form['name']
        parent=User.query.get(session['user_id'])
        parent_id=parent.id
        class_name = request.form['class']
        image_file = request.files['file']
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        student=Student(sname=name,parent_id=parent_id,clad=class_name,img=image_filename)
        db.session.add(student)
        db.session.commit() 
        flash('Registration successful!', 'success')
        return redirect(url_for('parent_dashboard'))


@app.route('/parent_demo_class_request/<int:teacher_id>', methods=['GET', 'POST'])
def parent_demo_class_request(teacher_id):
    if request.method == 'POST':
        teacher=Teacher.query.get(teacher_id)
        parent=User.query.get(session['user_id'])
        student_id=request.form['Student']
        print(student_id,'student id '*4)
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        status='pending'
        class_link=None
        demo_class_request = DemoClassRequest(teacher_id=teacher_id, parent_id=parent.id, student_id=student_id, demo_class_id=None, date=date, status=status, class_link=class_link)
        db.session.add(demo_class_request)
        db.session.commit()
        flash('Demo class request submitted successfully!', 'success')
        return redirect(url_for('parent_dashboard'))
    
@app.route('/demo_class_request')
def demo_class_request():
    parent=User.query.get(session['user_id'])
    demo_class_requests = DemoClassRequest.query.filter_by(parent_id=parent.id).all()
    return render_template('parent_side/demo_class_request.html', demo_class_requests=demo_class_requests)

@app.route('/parent_book_boookings/<int:book_id>')
def parent_book_boookings(book_id):
    book=Book.query.get(book_id)
    parent=User.query.get(session['user_id'])
    date=datetime.datetime.now().strftime('%Y-%m-%d')
    status='pending'
    book_request = BookBookings(parent_id=parent.id, book_id=book_id, date=date, status=status)
    db.session.add(book_request)
    db.session.commit()
    flash('Book request submitted successfully!', 'success')
    return redirect(url_for('parent_dashboard'))

@app.route('/book_teacher/<int:demo_class_request_id>/<int:teacher_id>',methods=['GET', 'POST'])
def book_teacher(demo_class_request_id,teacher_id):
        parent_id=session['user_id']
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        status='pending'
        book_request = TeacherBookings(demo_class_request_id=demo_class_request_id, parent_id=parent_id, teacher_id=teacher_id, date=date, status=status)
        db.session.add(book_request)
        db.session.commit()
        flash('Book request submitted successfully!', 'success')
        return redirect(url_for('parent_view_teacher_bookings'))

@app.route('/parent_view_teacher_bookings')
def parent_view_teacher_bookings():
    teacher_bookings=TeacherBookings.query.filter_by(parent_id=session['user_id']).all()
    return render_template('parent_side/teacher_booking.html',teacher_bookings=teacher_bookings)

@app.route('/mark_review',methods=['GET', 'POST'])
def mark_review():
    if request.method == 'POST':
        teacher=request.form['teacher']
        rateing1=rateing2=rateing3=rateing4=rateing5=False
        comment=request.form['review']
        if request.form.get('star1'):
            rateing1=True
        if request.form.get('star2'):
            rateing2=True
        if request.form.get('star3'):
            rateing3=True
        if request.form.get('star4'):
            rateing4=True
        if request.form.get('star5'):
            rateing5=True
        review=Review(rateing1=rateing1,rateing2=rateing2,rateing3=rateing3,rateing4=rateing4,rateing5=rateing5,comments=comment,user_id=session['user_id'],teacher_id=teacher)
        db.session.add(review)
        db.session.commit()
        if comment and rateing1 and rateing2 and rateing3 and rateing4 and rateing5:
            print(comment,rateing1,rateing2,rateing3,rateing4,rateing5)

        return redirect(url_for('_dashboard'))


#------------------------------teacher--------------------------------------

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))
    teacher=Teacher.query.get(session['teacher_id'])
    book=Book.query.all()
    return render_template('teacher_side/index.html',teacher=teacher,books=book)


@app.route('/add_demo_video', methods=['GET', 'POST'])
def add_demo_video():
    if request.method == 'POST':
        teacher_id = session['teacher_id']
        video_url = request.files['file']
        teacher = Teacher.query.get(teacher_id)
        subject = request.form['subject']
        class_details = request.form['class_details']
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        if video_url and video_url.filename:
            video_filename = secure_filename(video_url.filename)
            video_url.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))             
        demo=DemoClass(teacher_id=teacher_id,subject=subject,class_details=class_details,video=video_filename,date=date)
        db.session.add(demo)    
        db.session.commit()
        flash('Demo video added successfully!', 'success')
        return redirect(url_for('teacher_dashboard'))

@app.route('/view_demo_class_requests')
def view_demo_class_requests():
    teacher=Teacher.query.get(session['teacher_id'])
    demo=DemoClassRequest.query.filter_by(teacher_id=teacher.id)
    demo_class=DemoClass.query.filter_by(teacher_id=teacher.id)
    print(demo)
    return render_template('teacher_side/demo_class_request.html',demo_class_requests=demo,demo_class=demo_class)

@app.route('/assign_demo_class/<req_id>',methods=['POST'])
def Assign_demo_class(req_id):
    if request.method=='POST':
        demo_class_request=DemoClassRequest.query.get(req_id)
        demo_class_request.demo_class_id=request.form['demo_class']
        demo_class_request.class_link=request.form['link']
        demo_class_request.status='accepted'
        db.session.commit()
        return redirect(url_for('view_demo_class_requests'))

@app.route('/teacher_book_requests/<int:book_id>')
def teacher_book_requests(book_id):
    book=Book.query.get(book_id)
    teacher=Teacher.query.get(session['teacher_id'])
    date=datetime.datetime.now().strftime('%Y-%m-%d')
    status='pending'
    book_request = BookBookings(teacher_id=teacher.id, book_id=book_id, date=date, status=status)
    db.session.add(book_request)
    db.session.commit()    
    return redirect(url_for('teacher_dashboard'))

@app.route('/bookings',methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        time=request.form['time']
        booking_id=request.form['booking_id']
        print(booking_id)
        bookings=TeacherBookings.query.get(booking_id)
        bookings.time=time
        bookings.status='accepted'
        db.session.commit()
        return redirect(url_for('bookings'))
    teacher=Teacher.query.get(session['teacher_id'])
    teacher_bookings=TeacherBookings.query.filter_by(teacher_id=teacher.id).all()
    return render_template('teacher_side/bookings.html',teacher_bookings=teacher_bookings)


@app.route('/reject_teacher_bookings/<int:booking_id>')
def reject_teacher_bookings(booking_id):
    booking=TeacherBookings.query.get(booking_id)
    print(booking_id)

    print(booking)
    booking.status='rejected'
    db.session.commit()
    return redirect(url_for('bookings'))

@app.route('/reject_demo_class_request/<req_id>')   
def reject_demo_class_request(req_id):
    demo_class_request=DemoClassRequest.query.get(req_id)
    demo_class_request.status='rejected'
    db.session.commit()
    return redirect(url_for('view_demo_class_requests'))



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
