import pymysql


class Database:
    def __init__(self):
        # Connect using pymysql
        self.conn = pymysql.connect(
            host="localhost",
            user="root",         # replace with your user if needed
            password="beyourit@",  # replace with your password
            database="student_db",  # optional, returns dicts instead of tuples
        )

        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # students table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                grade VARCHAR(10)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        # users table for auth: role = 'admin' or 'student', optionally link to student_id
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin','student') NOT NULL,
                student_id INT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        self.conn.commit()
    def close_connection(self):
        try:
            self.cursor.close()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass
