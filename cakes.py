import os
import csv
import shutil

# Base directories for user data and uploaded files
USER_DATA_DIR = "./UserData"
FILES_DIR = "./Files"
os.makedirs(USER_DATA_DIR, exist_ok=True)
os.makedirs(FILES_DIR, exist_ok=True)

USERS_FILE = os.path.join(USER_DATA_DIR, "users.csv")

# Ensure the users.csv file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "password"])


def load_users():
    """Load user credentials from the CSV."""
    with open(USERS_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_user(user_id, username, password):
    """Save a new user to the CSV."""
    with open(USERS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, password])


def user_menu(username):
    """Menu for logged-in users."""
    print(f"\nWelcome, {username}!")
    user_files_file = os.path.join(USER_DATA_DIR, f"{username}_metadata.csv")

    # Ensure user-specific metadata file exists
    if not os.path.exists(user_files_file):
        with open(user_files_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "filename", "size", "path"])

    while True:
        print("\nMenu:")
        print("1. Upload File")
        print("2. View Uploaded Files")
        print("3. Delete File")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            upload_file(username, user_files_file)
        elif choice == "2":
            view_uploaded_files(user_files_file)
        elif choice == "3":
            delete_file(user_files_file)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def upload_file(username, user_files_file):
    """Move a file to the user's folder and save its metadata."""
    file_path = input("Enter the full path of the file to upload: ")

    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    # Move file to the `Files` directory with a unique name
    file_name = os.path.basename(file_path)
    user_folder = os.path.join(FILES_DIR, username)
    os.makedirs(user_folder, exist_ok=True)
    destination = os.path.join(user_folder, file_name)

    if os.path.exists(destination):
        print("A file with this name already exists. Rename the file and try again.")
        return

    shutil.move(file_path, destination)  # Move the original file to the user's folder

    # Collect metadata
    size = os.path.getsize(destination) // 1024  # Convert to KB

    # Save metadata to the user's metadata file
    with open(user_files_file, "a", newline="") as f:
        writer = csv.writer(f)
        file_id = sum(1 for _ in open(user_files_file))  # Count lines for ID
        writer.writerow([file_id, file_name, size, destination])

    print(f"File '{file_name}' uploaded successfully and stored in {destination}.")


def view_uploaded_files(user_files_file):
    """View uploaded files and their metadata."""
    with open(user_files_file, "r") as f:
        reader = csv.DictReader(f)
        files = list(reader)

    if files:
        print("\nYour Uploaded Files:")
        for file in files:
            print(f"ID: {file['id']} - Name: {file['filename']} - Size: {file['size']}KB")
    else:
        print("No files uploaded yet.")


def delete_file(user_files_file):
    """Delete a file and its metadata."""
    file_id = input("Enter the ID of the file to delete: ")

    with open(user_files_file, "r") as f:
        reader = csv.DictReader(f)
        files = list(reader)

    for file in files:
        if file["id"] == file_id:
            # Delete the file from the filesystem
            if os.path.exists(file["path"]):
                os.remove(file["path"])
                print(f"File '{file['filename']}' deleted successfully.")
            else:
                print(f"File '{file['filename']}' not found on disk.")

            # Update metadata
            files.remove(file)
            with open(user_files_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "filename", "size", "path"])
                writer.writeheader()
                writer.writerows(files)
            return

    print("File ID not found.")


def main():
    """Main function for the CLI."""
    while True:
        print("\nCAKES File Storage System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def register_user():
    """Register a new user."""
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    users = load_users()
    if any(user["username"] == username for user in users):
        print("Username already exists!")
        return

    user_id = len(users) + 1
    save_user(user_id, username, password)
    print("User registered successfully!")


def login_user():
    """Login an existing user."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            user_menu(username)
            return

    print("Invalid username or password.")


if __name__ == "__main__":
    main()
