from flask import Flask, request, redirect, render_template, flash, url_for
from flask_login import LoginManager, login_required, current_user
import os

app = Flask(__name__)
app.config['database uri goes here'] = 'sqlite:///cakes.db'
app.config['secret key goes here'] = os.urandom(24)

# Initialize the database
from models import db, User, FileUpload
db.init_app(app)

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Local directory for file storage
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create folder if it doesn't exist

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    """Route to handle file deletion."""
    file_upload = FileUpload.query.filter_by(id=file_id, user_id=current_user.id).first()
    if not file_upload:
        flash('File not found or you do not have permission to delete it.', 'danger')
        return redirect(url_for('upload_file'))  # Redirect to file list or upload page

    # Delete file from the file system
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{file_upload.filename}.enc')
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove file entry from the database
    db.session.delete(file_upload)
    db.session.commit()

    flash('File deleted successfully!', 'success')
    return redirect(url_for('upload_file'))  # Redirect to file list or upload page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creating the tables before running the app
    app.run(debug=True)
