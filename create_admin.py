# create_admin.py
from db import Database
from werkzeug.security import generate_password_hash
import getpass

db = Database()

username = input("Enter admin username: ").strip()
student = input("Enter student id: ").strip()
pw = getpass.getpass("Enter admin password: ")
pw2 = getpass.getpass("Confirm password: ")

if pw != pw2:
    print("Passwords don't match. Aborting.")
else:
    hashed = generate_password_hash(pw)
    try:
        db.cursor.execute(
            "INSERT INTO users (username, password, role, student_id) VALUES (%s, %s, 'student',%s)",
            (username, hashed, student)
        )
        db.conn.commit()
        print("Admin user created.")
    except Exception as e:
        print("Error:", e)
