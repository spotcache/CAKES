# CAKES: Command-Line File Management System

CAKES (Cicada Anonymous Key Escrow System) is a simplified command-line application for managing user accounts and securely storing their uploaded files. 

This version is designed to:
- Store user credentials and metadata in a `UserData` folder.
- Store uploaded files in a `Files/<username>/` folder.
- Provide essential features such as user registration, login, file upload, file viewing, and file deletion.

---

## Features

1. **User Management**:
   - Register new users with a unique username and password.
   - Login with existing credentials.

2. **File Management**:
   - Upload files (original files are moved to `Files/<username>`).
   - View metadata of uploaded files, including file name and size.
   - Delete files (removes both metadata and the file from storage).

3. **Folder Structure**:
   - User credentials and metadata are stored in `./UserData`.
   - Uploaded files are organized by user in `./Files`.
