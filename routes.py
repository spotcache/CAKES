from flask import app, request, redirect, render_template, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os
from models import db, User, FileUpload
from werkzeug.security import generate_password_hash, check_password_hash

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('upload_file'))
        else:
            flash('Login failed. Check your credentials.')

    return render_template('login.html')

# Upload File Route
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        timer_duration = request.form['duration']

        if not file:
            flash('No file selected.')
            return redirect(url_for('upload_file'))

        # Encrypt the file
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_file = cipher_suite.encrypt(file.read())

        # Save the encrypted file locally
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file.filename}.enc')
        with open(file_path, 'wb') as encrypted_file_obj:
            encrypted_file_obj.write(encrypted_file)

        # Store metadata in the database
        new_file = FileUpload(
            filename=file.filename,
            user_id=current_user.id,
            last_checkin=datetime.utcnow(),
            timer_duration=int(timer_duration)
        )
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded and encrypted successfully!')
        return redirect(url_for('upload_file'))

    return render_template('upload.html')

# Check-in Logic for auto-upload
def check_in(user_id):
    file_uploads = FileUpload.query.filter_by(user_id=user_id).all()
    for upload in file_uploads:
        if upload.last_checkin < datetime.utcnow() - timedelta(hours=upload.timer_duration):
            auto_upload(upload)

# Auto-upload action (local version)
def auto_upload(file_upload):
    # Path to the encrypted file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file_upload.filename}.enc')

    if os.path.exists(file_path):
        # Handle the auto-upload (local logic, could move the file, etc.)
        print(f"File {file_upload.filename} has been automatically processed.")

    else:
        print(f"Error: {file_upload.filename} not found.")
