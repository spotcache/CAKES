from flask import request, redirect, render_template, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from app import app, db, s3_client
from models import User, FileUpload

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

        # Store metadata in the database
        new_file = FileUpload(
            filename=file.filename,
            user_id=current_user.id,
            last_checkin=datetime.utcnow(),
            timer_duration=int(timer_duration)
        )
        db.session.add(new_file)
        db.session.commit()

        # Upload the encrypted file to AWS S3
        s3_client.put_object(
            Bucket='YOUR_BUCKET_NAME',
            Key=f'uploads/{new_file.id}.enc',
            Body=encrypted_file
        )

        flash('File uploaded successfully!')
        return redirect(url_for('upload_file'))

    return render_template('upload.html')

def check_in(user_id):
    file_uploads = FileUpload.query.filter_by(user_id=user_id).all()
    for upload in file_uploads:
        if upload.last_checkin < datetime.utcnow() - timedelta(hours=upload.timer_duration):
            auto_upload(upload)

def auto_upload(file_upload):
    # Retrieve the encrypted file from AWS S3
    try:
        response = s3_client.get_object(
            Bucket='YOUR_BUCKET_NAME',
            Key=f'uploads/{file_upload.id}.enc'
        )
        encrypted_file_data = response['Body'].read()

        # We could upload to another service or change its permissions
        # For demonstration, we'll change the S3 file's ACL to public-read
        s3_client.put_object_acl(
            Bucket='YOUR_BUCKET_NAME',
            Key=f'uploads/{file_upload.id}.enc',
            ACL='public-read'  # Make it publicly accessible
        )

        # Log or notify that the file has been auto-uploaded
        print(f"File {file_upload.filename} auto-uploaded and made public.")
        # Optionally, sending an email notification to the user (not implemented here)

    except Exception as e:
        print(f"Error during auto-upload: {e}")
