import psycopg2
import random


class Database:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as err:
            print(f"Error connecting to the database: {err}")
            print("Please check your database credentials or ensure the server is running.")
            exit(1)  # Exit the program if the connection fails
        except Exception as err:
            print(f"Unexpected error during database connection: {err}")
            exit(1)

    def execute(self, query, params=None):
        try:
            self.cur.execute(query, params)
        except Exception as err:
            print(f"Error executing query: {err}")
            self.conn.rollback()

    def executemany(self, query, params):
        try:
            self.cur.executemany(query, params)
        except Exception as err:
            print(f"Error executing multiple queries: {err}")
            self.conn.rollback()

    def commit(self):
        try:
            self.conn.commit()
        except Exception as err:
            print(f"Error during commit: {err}")

    def close(self):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as err:
            print(f"Error closing the connection: {err}")


class SchemaCreator:
    def __init__(self, db):
        self.db = db

    def create_schema(self):
        try:
            self.db.execute("""
                CREATE SCHEMA IF NOT EXISTS students_report_system;
            """)

            self.db.execute("""
                CREATE TABLE IF NOT EXISTS students_report_system.students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER NOT NULL
                );
            """)

            self.db.execute("""
                CREATE TABLE IF NOT EXISTS students_report_system.courses (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    code VARCHAR(50) UNIQUE NOT NULL,
                    credits INTEGER NOT NULL
                );       
            """)

            self.db.execute("""
                CREATE TABLE IF NOT EXISTS students_report_system.grades (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students_report_system.students(id) ON DELETE CASCADE,
                    course_id INTEGER NOT NULL REFERENCES students_report_system.courses(id) ON DELETE CASCADE,
                    grade VARCHAR(2) NOT NULL
                );
            """)

            self.db.commit()
        except Exception as err:
            print(f"Error: {err}")
            self.db.conn.rollback()


class DataInserter:
    def __init__(self, db):
        self.db = db

    def insert_data(self):
        student_names = [
            "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Evans", "Edward Wilson",
            "Fiona Green", "George Adams", "Hannah Clarke", "Ian Taylor", "Jane Miller",
            "Kevin Anderson", "Laura Scott", "Michael Moore", "Nina Harris", "Oliver Lee",
            "Paul Walker", "Quinn Hall", "Rachel White", "Sam Turner", "Tina Lewis",
            "Uma Davis", "Victor Allen", "Wendy Young", "Xander King", "Yvonne Martinez"
        ]
        students_data = [(name, 18 + (i % 5)) for i, name in enumerate(student_names)]

        courses_data = [
            ("Mathematics", "MATH101", 3),
            ("Physics", "PHYS101", 4),
            ("Chemistry", "CHEM101", 4),
            ("Biology", "BIO101", 3),
            ("Computer Science", "CS101", 4),
        ]
        try:
            self.db.execute("SELECT COUNT(*) FROM students_report_system.students")
            if self.db.cur.fetchone()[0] == 0:
                self.db.executemany("""
                    INSERT INTO students_report_system.students (name, age)
                    VALUES (%s, %s)
                """, students_data)

            self.db.execute("SELECT COUNT(*) FROM students_report_system.courses")
            if self.db.cur.fetchone()[0] == 0:
                self.db.executemany("""
                    INSERT INTO students_report_system.courses (name, code, credits)
                    VALUES (%s, %s, %s)
                """, courses_data)

            self.db.execute("SELECT COUNT(*) FROM students_report_system.grades")
            if self.db.cur.fetchone()[0] == 0:
                
                self.db.execute("SELECT id FROM students_report_system.students")
                student_ids = [row[0] for row in self.db.cur.fetchall()]

                self.db.execute("SELECT id FROM students_report_system.courses")
                course_ids = [row[0] for row in self.db.cur.fetchall()]

                grades_data = [
                (student_id, course_id, random.choice(["A", "B", "C", "D", "F"]))
                for student_id in student_ids
                for course_id in random.sample(course_ids, random.randint(1, len(course_ids)))
                ]

                self.db.executemany("""
                    INSERT INTO students_report_system.grades (student_id, course_id, grade)
                    VALUES (%s, %s, %s)
                """, grades_data)

            self.db.commit()
        except Exception as err:
            print(f"Error: {err}")
            self.db.conn.rollback()



