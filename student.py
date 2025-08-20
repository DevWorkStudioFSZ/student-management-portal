# student.py
from db import Database

class Student(Database):
    def __init__(self):
        super().__init__()

    def add(self, name, age, grade):
        sql = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (name, age, grade))
        self.conn.commit()
        return self.cursor.lastrowid

    def view_all(self):
        self.cursor.execute("SELECT * FROM students ORDER BY id ASC")
        return self.cursor.fetchall()

    def get(self, sid):
        self.cursor.execute("SELECT * FROM students WHERE id = %s", (sid,))
        return self.cursor.fetchone()

    def update(self, sid, name, age, grade):
        sql = "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s"
        self.cursor.execute(sql, (name, age, grade, sid))
        self.conn.commit()

    def delete(self, sid):
        sql = "DELETE FROM students WHERE id=%s"
        self.cursor.execute(sql, (sid,))
        self.conn.commit()
