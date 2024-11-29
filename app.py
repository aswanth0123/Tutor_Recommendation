from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import *  # Import models from models.py
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = '43e77e90e26e1ddee83ea02b35065b805630944d4bd13d3abcbd120627d308a9' # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Project:Project123@localhost/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads/'  # Directory to store uploaded files
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
@login_required
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
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('No file uploaded.', 'danger')
            return redirect(request.url)

        # Create and save new teacher instance
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

@app.route('/add_book')
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
        return redirect(url_for('list_books')) 
    return render_template('admin_side/add_book.html')

@app.route('/admin_view_books')
@login_required
def admin_view_books():
    books = Book.query.all()
    return render_template('admin_side/view_books.html', books=books)

@app.route('/index')
def index():
    return render_template('index.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
