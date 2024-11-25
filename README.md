## CAKES: Cicada Anonymous Key Escrow System

CAKES is a secure system designed for privacy/security minded users who need to anonymously upload/access sensitive files to the internet. The system allows users to set a timer, and if they fail to check in, the file is automatically uploaded to a public platform.

## Contains

- User registration and authentication.
- Secure file upload with encryption.
- Automatic file sharing after a specified duration.
- Integration with AWS S3 for file storage.
- User notifications (optional).

## Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Cryptography
- Boto3 (AWS SDK for Python)
- SQLite (or any other database supported by SQLAlchemy)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/spotcache/CAKES.git
   cd CAKES
   ```
Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required packages:
```
pip install -r requirements.txt
```
Set your AWS credentials: Update the s3_client configuration in app.py with your AWS access key and secret key.

Create the database:

Run the following command to create the SQLite database:
```
python -c "from app import db; db.create_all()"
```
Usage:
Run the application:
```
python app.py
```
Access the application: Open your web browser and navigate to http://127.0.0.1:5000.

Register an account: Click on the registration link to create a new user account.

Log in: After registration, log in with your credentials.

Upload files: Go to the upload section to upload sensitive files, set a timer, and monitor your uploads.

Auto-upload Logic:
If a user fails to check in or specify other instructions before the specified duration, the system will automatically make the file public by changing its permissions in AWS S3. This feature is crucial for ensuring that critical information is shared when needed.

Security Considerations:
All uploaded files are encrypted before being stored in S3.
Ensure that you manage your AWS credentials securely and avoid hardcoding sensitive information in the source code.

Contributing:
If you'd like to contribute to CAKES, please fork the repository and submit a pull request with your changes.

License:
This project is licensed under the MIT License - see the LICENSE file for details.

Contact:
For any questions or inquiries, please contact:

spotcache -
spotcache@gmail.com

cunningidiot -
eveisanidiot@gmail.com
