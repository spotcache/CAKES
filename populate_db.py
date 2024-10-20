from models import db, User, FileUpload
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app

# Initialize the app context
with app.app_context():
    # Create all tables
    db.create_all()

    # Add a test user
    user1 = User(username='testuser', password=generate_password_hash('password123'))

    # Add a test file upload for this user
    file1 = FileUpload(
        filename='secret_file.txt',
        user_id=1,  # Assuming testuser has id=1
        last_checkin=datetime.utcnow(),
        timer_duration=24  # 24 hours
    )

    # Commit the changes
    db.session.add(user1)
    db.session.add(file1)
    db.session.commit()

    print("Example data added to cakes.db")
