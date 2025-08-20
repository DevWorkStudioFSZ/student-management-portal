# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from student import Student
from db import Database
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecret"  # change this in production
student = Student()
db = Database()

# -----------------------
# Authentication routes
# -----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash("Enter both username and password.", "warning")
            return redirect(url_for('login'))

        db.cursor.execute("SELECT id, username, password, role, student_id FROM users WHERE username=%s", (username,))
        user = db.cursor.fetchone()
        if user and (user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            session['student_id'] = user[4]  # None for admins
            flash(f"Welcome, {user[1]}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for('login'))

# -----------------------
# Dashboard route
# -----------------------
@app.route('/')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))

    if session['role'] == 'admin':
        students = student.view_all()
        return render_template('index.html', students=students)
    else:  # student role
        sid = session.get('student_id')
        if sid is None:
            flash("No student record linked to your account.", "warning")
            return redirect(url_for('logout'))
        data = student.get(sid)
        return render_template('student_view.html', student=data)

# -----------------------
# Admin-only CRUD routes
# -----------------------
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("Admin access required.", "danger")
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

@app.route('/add', methods=['POST'])
@admin_required
def add_student():
    name = request.form.get('name', '').strip()
    age = request.form.get('age', '').strip()
    grade = request.form.get('grade', '').strip()
    if not name or not age or not grade:
        flash("All fields required.", "warning")
        return redirect(url_for('dashboard'))
    try:
        sid = student.add(name, int(age), grade)
        flash("Student added successfully.", "success")
        # optional: if form included an option to create user for this student, you could create here
    except Exception as e:
        flash("Error adding student: " + str(e), "danger")
    return redirect(url_for('dashboard'))

@app.route('/update/<int:sid>', methods=['GET', 'POST'])
@admin_required
def update_student(sid):
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        grade = request.form.get('grade', '').strip()
        if not name or not age or not grade:
            flash("All fields required.", "warning")
            return redirect(url_for('update_student', sid=sid))
        try:
            student.update(sid, name, int(age), grade)
            flash("Student updated.", "success")
        except Exception as e:
            flash("Error updating student: " + str(e), "danger")
        return redirect(url_for('dashboard'))

    data = student.get(sid)
    if not data:
        flash("Student not found.", "warning")
        return redirect(url_for('dashboard'))
    return render_template('update.html', student=data)

@app.route('/delete/<int:sid>', methods=['POST'])
@admin_required
def delete_student(sid):
    try:
        # also clear any users linked to this student (optional)
        db.cursor.execute("UPDATE users SET student_id = NULL WHERE student_id = %s", (sid,))
        student.delete(sid)
        flash("Student deleted.", "danger")
    except Exception as e:
        flash("Error deleting student: " + str(e), "danger")
    return redirect(url_for('dashboard'))
@app.route('/generate_credentials', methods=['POST'])
@admin_required
def generate_credentials():
    student_id = request.form.get('student_id')
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm', '')
    
    # Validate inputs
    if not student_id or not username or not password or not confirm:
        flash("All fields are required.", "warning")
        return redirect(url_for('dashboard'))
        
    if password != confirm:
        flash("Passwords don't match.", "warning")
        return redirect(url_for('dashboard'))
    
    try:
        # Verify student exists
        student_data = student.get(student_id)
        if not student_data:
            flash("Student not found.", "danger")
            return redirect(url_for('dashboard'))
        
        # Hash password
        hashed_pw = generate_password_hash(password)
        
        # Create user account
        db.cursor.execute(
            "INSERT INTO users (username, password, role, student_id) VALUES (%s, %s, 'student', %s)",
            (username, hashed_pw, student_id)
        )
        db.conn.commit()
        
        flash(f"Credentials created for {student_data[1]}!", "success")
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            flash("Username already exists. Please choose a different username.", "danger")
        else:
            flash(f"Error creating credentials: {str(err)}", "danger")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for('dashboard'))


# -----------------------
# Optional: admin page to create student user account
# (not included in UI by default; you can add a form)
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
