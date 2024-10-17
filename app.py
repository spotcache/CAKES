from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os
import boto3 # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cakes.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

s3_client = boto3.client('s3', 
    aws_access_key_id='YOUR_AWS_ACCESS_KEY',
    aws_secret_access_key='YOUR_AWS_SECRET_KEY'
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_checkin = db.Column(db.DateTime)
    timer_duration = db.Column(db.Integer)  # in hours

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
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_file = cipher_suite.encrypt(file.read())

        new_file = FileUpload(
            filename=file.filename,
            user_id=current_user.id,
            last_checkin=datetime.utcnow(),
            timer_duration=int(timer_duration)
        )
        db.session.add(new_file)
        db.session.commit()

        # Save encrypted file to AWS S3
        s3_client.put_object(
            Bucket='YOUR_BUCKET_NAME',
            Key=f'uploads/{new_file.id}.enc',
            Body=encrypted_file
        )

        return redirect('/success')

    return render_template('upload.html')

def check_in(user_id):
    file_uploads = FileUpload.query.filter_by(user_id=user_id).all()
    for upload in file_uploads:
        if upload.last_checkin < datetime.utcnow() - timedelta(hours=upload.timer_duration):
            auto_upload(upload)

def auto_upload(file_upload):
    # Logic for auto-uploading the file
    pass

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
