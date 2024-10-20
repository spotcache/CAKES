from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os
import boto3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cakes.db'
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize the database
from models import db, User, FileUpload
db.init_app(app)

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# AWS S3 configuration
s3_client = boto3.client('s3', 
    aws_access_key_id='YOUR_AWS_ACCESS_KEY',
    aws_secret_access_key='YOUR_AWS_SECRET_KEY'
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rest of the routes (register, login, upload_file, etc.)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creating the tables before running the app
    app.run(debug=True)
