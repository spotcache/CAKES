from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import boto3

# Initialize app and configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cakes.db'
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# AWS S3 configuration
s3_client = boto3.client(
    's3',
    aws_access_key_id='AWS_ACCESS_KEY',
    aws_secret_access_key='AWS_SECRET_KEY'
)

from models import User, FileUpload
from routes import *

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
