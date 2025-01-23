from db_handler import Database, SchemaCreator, DataInserter
from operations import Operations
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    config = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
    }
    db = Database(config)
    db.connect()
    schema_creator = SchemaCreator(db)
    schema_creator.create_schema()
    data_inserter = DataInserter(db)
    data_inserter.insert_data()
    operations = Operations(db)

    print("Welcome to the Students Report System!")
    while True:
        choice_1 = input("\nType 'S' to list students, 'C' to list courses or 'Q' to quit: ")
        if choice_1.lower() == 's':
            operations.list_students()
            while True:
                student_id = input("Enter student ID to search or 'Q' to quit to the menu: ")
                if not student_id:
                    continue
                elif student_id.isdigit():
                    student_id = int(student_id)
                    if operations.student_exists(student_id):
                        operations.search_student_by_id(student_id)
                        break
                    else:
                        print("This student ID is not in the system.")
                elif student_id.lower() == 'q':
                    break
                else:
                    print("Invalid input. Please enter a number as ID!")

        elif choice_1.lower() == 'c':
            operations.list_courses()
            while True:
                course_id = input("Enter course ID to search or 'Q' to quit to the menu: ")
                if not course_id:
                    continue
                elif course_id.isdigit():
                    course_id = int(course_id)
                    if operations.course_exists(course_id):
                        operations.search_course_by_id(course_id)
                        break
                    else:
                        print("This course ID is not in the system.")
                elif course_id.lower() == 'q':
                    break
                else:
                    print("Invalid input. Please enter a number as ID!")

        elif choice_1.lower() == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please only choose from 'S','C' or 'Q'!")

    db.close()

if __name__ == '__main__':
    main()