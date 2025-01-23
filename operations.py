class Operations:
    def __init__(self, db):
        self.db = db

    def list_students(self):
        try:
            self.db.execute("SELECT id, name, age FROM students_report_system.students;")
            students = self.db.cur.fetchall()
            print("Students:")
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}")
        except Exception as err:
            print(f"Error: {err}")

    def list_courses(self):
        try:
            self.db.execute("SELECT id, name, code, credits FROM students_report_system.courses;")
            courses = self.db.cur.fetchall()
            print("Courses:")
            for course in courses:
                print(f"ID: {course[0]}, Name: {course[1]}, Code: {course[2]}, Credits: {course[3]}")
        except Exception as err:
            print(f"Error: {err}")

    def search_student_by_id(self, student_id):
        grade_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1}  
        try:
            self.db.execute("""
                SELECT students_report_system.students.id, 
                    students_report_system.students.name, 
                    students_report_system.students.age
                FROM students_report_system.students
                WHERE students_report_system.students.id = %s
            """, (student_id,))
            student = self.db.cur.fetchone()

            if student:
                print(f"\nStudent Details:")
                print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}")
                self.db.execute("""
                    SELECT students_report_system.courses.name AS course_name, 
                        students_report_system.grades.grade
                    FROM students_report_system.grades
                    JOIN students_report_system.courses 
                    ON students_report_system.grades.course_id = students_report_system.courses.id
                    WHERE students_report_system.grades.student_id = %s
                """, (student_id,))
                courses = self.db.cur.fetchall()

                if courses:
                    print("\nCourses and Grades:")
                    numerical_grades = []
                    for course in courses:
                        grade_numeric = grade_map[course[1]]
                        numerical_grades.append(grade_numeric)
                        print(f"  {course[0]}: {course[1]}")

                    average = sum(numerical_grades) / len(numerical_grades)
                    print(f"\nAverage Grade: {average:.2f}")
                else:
                    print("\nThis student is not enrolled in any courses.")
            else:
                print(f"No student found with ID {student_id}.")
        except Exception as err:
            print(f"Error searching for student: {err}")

    def search_course_by_id(self, course_id):
        grade_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1}  
        try:
            self.db.execute("""
                SELECT students_report_system.courses.id, 
                    students_report_system.courses.name, 
                    students_report_system.courses.code, 
                    students_report_system.courses.credits
                FROM students_report_system.courses
                WHERE students_report_system.courses.id = %s
            """, (course_id,))
            course = self.db.cur.fetchone()

            if course:
                print(f"\nCourse Details:")
                print(f"ID: {course[0]}, Name: {course[1]}, Code: {course[2]}, Credits: {course[3]}")
                self.db.execute("""
                    SELECT students_report_system.grades.grade
                    FROM students_report_system.grades
                    WHERE students_report_system.grades.course_id = %s
                """, (course_id,))
                grades = self.db.cur.fetchall()

                if grades:
                    numerical_grades = [grade_map[grade[0]] for grade in grades if grade[0] in grade_map]
                    average = sum(numerical_grades) / len(numerical_grades)
                    print(f"\nAverage Grade for the Course: {average:.2f}")

                self.db.execute("""
                    SELECT students_report_system.students.id AS student_id, 
                        students_report_system.students.name AS student_name, 
                        students_report_system.grades.grade
                    FROM students_report_system.grades
                    JOIN students_report_system.students 
                    ON students_report_system.grades.student_id = students_report_system.students.id
                    WHERE students_report_system.grades.course_id = %s
                """, (course_id,))
                students = self.db.cur.fetchall()

                if students:
                    print("\nEnrolled Students and Grades:")
                    for student in students:
                        print(f"  Student ID: {student[0]}, Name: {student[1]}, Grade: {student[2]}")
                else:
                    print("\nNo students are enrolled in this course.")
            else:
                print(f"No course found with ID {course_id}.")
        except Exception as err:
            print(f"Error searching for course: {err}")

    def student_exists(self, student_id):
        try:
            self.db.execute("""
                SELECT 1 FROM students_report_system.students WHERE id = %s;
            """, (student_id,))
            return self.db.cur.fetchone() is not None
        except Exception as err:
            print(f"Error checking if student exists: {err}")
            return False
        
    def course_exists(self, course_id):
        try:
            self.db.execute("""
                SELECT 1 FROM students_report_system.courses WHERE id = %s;
            """, (course_id,))
            return self.db.cur.fetchone() is not None
        except Exception as err:
            print(f"Error checking if course exists: {err}")
            return False