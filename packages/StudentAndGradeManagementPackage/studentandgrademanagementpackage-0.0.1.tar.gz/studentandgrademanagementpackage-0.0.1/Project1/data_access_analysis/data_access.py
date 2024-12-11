import csv
import pandas as pd
import matplotlib.pyplot as plt
from person.student import Student
from person.teacher import Teacher
from grade_management.course import Course
from grade_management.grade import Grade
from encryption import Encryption

class DataAccess:
    students_list = []
    teachers_list = []
    courses_list = []
    grades_list = []
    user_credentials = {} #for storing the students and teacher's information

    @staticmethod
    def add_student():
        while True:
            try:
                student_id = input("Input student ID (or '-1' to end): ").strip()
                if student_id == "-1":
                    break
                name = input("Input student name: ").strip()
                gender = input("Input student gender (M/F): ").strip().upper()

                existing_student = next((s for s in DataAccess.students_list if s.student_id == student_id), None)

                if existing_student:
                    print(f"Student ID {student_id} already exists.")
                    choice = input("Do you want to overwrite this student? (Y/N): ").strip().lower()
                    if choice == "y":
                        existing_student.name = name
                        existing_student.gender = "Male" if gender == "M" else "Female"
                        print(f"Student with ID {student_id} updated successfully!")
                    elif choice == "n":
                        print("Student addition cancelled. Please input a new student ID.")
                    else:
                        print("Invalid choice. Please try again.")
                else:
                    student = Student(name, "Male" if gender == "M" else "Female", student_id)
                    DataAccess.students_list.append(student)
                    print("Student added successfully!")
            except ValueError:
                print("Please input valid data.")

    @staticmethod
    def add_teacher():
        while True:
            try:
                teacher_id = input("Input teacher ID (or '-1' to end): ")
                if teacher_id == "-1":
                    break
                name = input("Input teacher name: ")
                login_name = input("Input teacher login name: ")
                password = input("Input teacher password: ")
                if not teacher_id:
                    print("[DEBUG] Invalid teacher ID.")
                    continue

                if not name:
                    print("[DEBUG] Teacher name cannot be empty.")
                    continue
                
                existing_teacher = next((t for t in DataAccess.teachers_list if t.teacher_id == teacher_id), None)

                if existing_teacher:
                    print(f"Teacher ID {teacher_id} already exists.")
                    while True:
                        choice = input("Do you want to overwrite this teacher? (Y/N): ").strip().lower()
                        if choice == 'y':
                            existing_teacher.name = name
                            existing_teacher.login_name = login_name
                            existing_teacher.password = Encryption.encrypt(password)
                            print(f"Teacher with ID {teacher_id} updated successfully!")
                            break
                        elif choice == 'n':
                            print("Existing Teacher IDs: ", [t.teacher_id for t in DataAccess.teachers_list])
                            print("Please input a new teacher ID.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    teacher = Teacher(name=name, teacher_id=teacher_id, login_name=login_name, password=password)
                    DataAccess.teachers_list.append(teacher)
                    print("Teacher added successfully!")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                
    @staticmethod
    def import_user_credentials(file_path):
        """from CSV into id and password"""
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user_id = row['ID']
                    name = row['Name']
                    password = str(row['Password'])
                    role = row['Role']

                    # Encrypt the password before storing it
                    encrypted_password = Encryption.encrypt(password)

                    DataAccess.user_credentials[user_id] = {
                        'name': name,
                        'password': encrypted_password,
                        'role': role
                    }
            print(f"User credentials imported successfully from {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error occurred during import: {e}")
        

    @staticmethod
    def validate_student(student_id, password):
        """
        Validates a student's credentials.
        
        Parameters:
            student_id (str): The ID of the student.
            password (str): The input password to validate.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        user = DataAccess.user_credentials.get(student_id)
        if user and user['role'] == 'Student':
            password = str(password)
            decrypted_password = Encryption.decrypt(user['password'])
            print(f"Student Validation - Input ID: {student_id}, Input Password: {password}")

            return decrypted_password == password
        print(f"Student Login - User not found or incorrect role: {student_id}")
        return False

    @staticmethod
    def validate_teacher(teacher_id, password):
        """
        Validates a teacher's credentials.
        
        Parameters:
            teacher_id (str): The ID of the teacher.
            password (str): The input password to validate.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        user = DataAccess.user_credentials.get(teacher_id)
        if user and user['role'] == 'Teacher':
            password = str(password)
            decrypted_password = Encryption.decrypt(user['password'])
            print(f"Teacher Login - Input Password: {password}, Decrypted Password: {decrypted_password}")
            return decrypted_password == password
        print(f"Teacher Login - User not found or incorrect role: {teacher_id}")
        return False

    @staticmethod
    def add_course():
        while True:
            try:
                course_id = input("Input course ID (or '-1' to end): ").strip()
                if course_id == "-1":
                    break
                course_name = input("Input course name: ").strip()

                existing_course = next((c for c in DataAccess.courses_list if c.course_id == course_id), None)

                if existing_course:
                    print(f"Course ID {course_id} already exists.")
                    while True:
                        choice = input("Do you want to overwrite this course? (Y/N): ").strip().lower()
                        if choice == 'y':
                            existing_course.course_name = course_name
                            print(f"Course with ID {course_id} updated successfully!")
                        elif choice == 'n':
                            print("Existing Course IDs: ", [c.course_id for c in DataAccess.courses_list])
                            print("Please input a new course ID.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    course = Course(course_name=course_name, course_id=course_id)
                    DataAccess.courses_list.append(course)
                    print("Course added successfully!")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    @staticmethod
    def add_grade():
        while True:
            try:
                student_id = input("Enter Student ID (or '-1' to end): ").strip()
                if student_id == "-1":
                    break
                course_id = input("Enter Course ID: ").strip()
                grade_value = float(input("Enter Grade Value (0-100): ").strip())

                if not (0 <= grade_value <= 100):
                    print("Grade value must be between 0 and 100. Please try again.")
                    continue

                existing_grade = next(
                    (g for g in DataAccess.grades_list if g.student_id == student_id and g.course_id == course_id),
                    None
                )

                if existing_grade:
                    print(f"Grade for Student ID {student_id} in Course ID {course_id} already exists.")
                    while True:
                        choice = input("Do you want to overwrite this grade? (Y/N): ").strip().lower()
                        if choice == 'y':
                            existing_grade.grade_value = grade_value
                            print(f"Grade for Student ID {student_id} in Course ID {course_id} updated successfully!")
                        elif choice == 'n':
                            print("Existing Grades: ", [
                                (g.student_id, g.course_id) for g in DataAccess.grades_list
                            ])
                            print("Please input a new combination of Student ID and Course ID.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    grade = Grade(student_id=student_id, course_id=course_id, grade_value=grade_value)
                    DataAccess.grades_list.append(grade)
                    print("Grade added successfully!")
            except ValueError:
                print("Invalid grade value. Please input a number.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    @staticmethod
    def list_all_students():
        if not DataAccess.students_list:
            print("No students found.")
        else:
            for student in DataAccess.students_list:
                print(student)

    @staticmethod
    def list_all_teachers():
        if not DataAccess.teachers_list:
            print("No teachers found.")
        else:
            for teacher in DataAccess.teachers_list:
                print(teacher)

    @staticmethod
    def list_all_courses():
        if not DataAccess.courses_list:
            print("No courses found.")
        else:
            for course in DataAccess.courses_list:
                print(course)

    @staticmethod
    def list_all_grades():
        if not DataAccess.grades_list:
            print("No grades found.")
        else:
            for grade in DataAccess.grades_list:
                print(grade)

    @staticmethod
    def get_student_by_id(student_id):

        for student in DataAccess.students_list:
            if student.student_id == student_id:
                print(student)
                return
        print("Student not found.")

    @staticmethod
    def get_grade_by_student_and_course(student_id, course_id):

        for grade in DataAccess.grades_list:
            if grade.student_id == student_id and grade.course_id == course_id:
                print(f"Grade found: {grade}")
                return
        print("No grade found for the given student ID and course ID.")


    def get_teacher_by_id(teacher_id):

        for teacher in DataAccess.teachers_list:
            if teacher.teacher_id == teacher_id:
                print(teacher)
                return
        print("Teacher not found.")

    @staticmethod
    def get_course_by_id(course_id):

        for course in DataAccess.courses_list:
            if course.course_id == course_id:
                print(course)
                return
        print("Course not found.")

    @staticmethod
    def get_grades_by_student_id(student_id):

        found = False
        for grade in DataAccess.grades_list:
            if grade.student_id == student_id:
                print(grade)
                found = True
        if not found:
            print(f"No grades found for the student with ID: {student_id}.")

    @staticmethod
    def import_all_data_from_csv(file_path):
        """import student, course, and grade data from a single CSV file and associate it with existing lists."""
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
     
                    student_id = row.get('Student_ID')
                    student_name = row.get('Student_Name', None)
                    student_gender = row.get('Gender', 'Unknown')
                    course_id = row.get('Course_ID')
                    course_name = row.get('Course_Name', 'Unknown')
                    grade_value = row.get('Grade_Value')
                    teacher_id = row.get('Teacher_ID')
                    teacher_name = row.get('Teacher_Name', None)

                    
                    if student_id and not any(s.student_id == student_id for s in DataAccess.students_list):
                        student = Student(name=student_name or "Unnamed Student", gender=student_gender, student_id=student_id)
                        DataAccess.students_list.append(student)
                    
                    if teacher_id and not any(t.teacher_id == teacher_id for t in DataAccess.teachers_list):
                        if teacher_name is None:
                            teacher_name = f"Teacher_{teacher_id}"

                        teacher = Teacher(
                            name=teacher_name, 
                            teacher_id=teacher_id,
                            login_name=teacher_id,
                            password="default_password" 
                        )
                        DataAccess.teachers_list.append(teacher)
                     

                    
                    if course_id and not any(c.course_id == course_id for c in DataAccess.courses_list):
                        course = Course(course_name=course_name, course_id=course_id)
                        DataAccess.courses_list.append(course)
                        
                        
                    if grade_value and student_id and course_id:
                        if not any(
                            g.student_id == student_id and g.course_id == course_id
                            for g in DataAccess.grades_list
                        ):
                            grade = Grade(student_id=student_id, course_id=course_id, grade_value=float(grade_value))
                            DataAccess.grades_list.append(grade)
                        
                
                print(f"Data imported successfully from {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error occurred during import: {e}")
            
    @staticmethod
    def get_statistics(course_id):
        for grade in DataAccess.grades_list:
            print(f"Student ID: {grade.student_id}, Course ID: {grade.course_id}, Grade: {grade.grade_value}")

        grades = [g.grade_value for g in DataAccess.grades_list if g.course_id.strip() == course_id.strip()]
        if not grades:
            print(f"No grades available for Course ID {course_id}.")
            return

        df_grades = pd.DataFrame(grades, columns=["grade_value"])
        median_grade = df_grades["grade_value"].median()
        max_grade = df_grades["grade_value"].max()
        min_grade = df_grades["grade_value"].min()

        print(f"\nStatistics for Course ID {course_id}:")
        print(f"Median: {median_grade}")
        print(f"Max: {max_grade}")
        print(f"Min: {min_grade}")

        plt.figure(figsize=(6, 4))
        plt.boxplot(df_grades["grade_value"], vert=False)
        plt.title(f"Boxplot of Grades for Course ID {course_id}")
        plt.xlabel("Grade Value")
        plt.show()

    @staticmethod
    def get_grade_and_statistics(student_id, course_id):
        print(f"Searching for Student ID: '{student_id}' and Course ID: '{course_id}'")
            
        found_grade = next(
            (g for g in DataAccess.grades_list if g.student_id.strip() == student_id.strip() and g.course_id.strip() == course_id.strip()),
            None
        )

        if found_grade:
            print(f"Found Grade: Student ID {found_grade.student_id}, Course ID {found_grade.course_id}, Grade {found_grade.grade_value}")
            DataAccess.get_statistics(course_id)
        else:
            print(f"No grade found for Student ID: {student_id} and Course ID: {course_id}.")