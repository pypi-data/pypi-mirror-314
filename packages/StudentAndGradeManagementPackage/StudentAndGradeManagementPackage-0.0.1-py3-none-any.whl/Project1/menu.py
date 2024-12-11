from grade_management.grade import Grade
from data_access_analysis.data_access import DataAccess
from data_access_analysis.data_analysis import DataAnalysis

def login():
    while True:
        print("***** Welcome to the System *****")
        print("1: Student Login")
        print("2: Teacher Login")
        print("0: Exit")
        choice = input("Please select an option: ").strip()
        # print(f"[DEBUG] User entered: {choice}")  # Debug information
        if choice == "1":
            student_id = input("Enter your student ID: ").strip()
            password = input("Enter your password: ").strip()
            if DataAccess.validate_student(student_id, password):
                student_menu(student_id)
            else:
                print("Invalid student ID or password.")
        elif choice == "2":
            teacher_id = input("Enter your teacher ID: ").strip()
            password = input("Enter your password: ").strip()
            if DataAccess.validate_teacher(teacher_id, password):
                teacher_menu()
            else:
                print("Invalid teacher ID or password.")
        elif choice == "0":
            print("Exiting the program...")
            break
        else:
            print("Invalid option. Please try again.")

def student_menu(student_id):
    while True:
        print("***** Student Menu *****")
        print("1: View my information")
        print("2: View my grades")
        print("3: View my grades and data analysis")
        print("0: Logout")
        choice = input("Please select an option: ").strip()
        # print(f"[DEBUG] User entered: {choice}")  # Debug information
        if choice == "1":
            DataAccess.get_student_by_id(student_id)
        elif choice == "2":
            DataAccess.get_grades_by_student_id(student_id)
        elif choice == "3":
            grade_analysis_menu(student_id)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

def grade_analysis_menu(student_id):
    while True:
        print("***** Grades and Data Analysis *****")
        print("1: Display average grade")
        print("2: Convert grades to GPA")
        print("3: Analyze grades for a specific course")
        print("0: Back to Student Menu")
        sub_choice = input("Please select an option: ").strip()
        # print(f"[DEBUG] User entered: {sub_choice}")  # Debug information
        if sub_choice == "1":
            DataAnalysis.display_average_grade(student_id)
        elif sub_choice == "2":
            DataAnalysis.convert_grades_to_gpa(student_id)
        elif sub_choice == "3":
            course_id = input("Enter the course ID: ").strip()
            DataAccess.get_statistics(course_id)
        elif sub_choice == "0":
            print("Returning to Student Menu...")
            break
        else:
            print("Invalid option. Please try again.")

def teacher_menu():
    # print("[DEBUG] Entering teacher_menu...")  # Debug information
    while True:
        print("***** Teacher Menu *****")
        print("1: Add a student")
        print("2: Add a course")
        print("3: Add a teacher")
        print("4: Add a grade")
        print("5: List all students")
        print("6: List all courses")
        print("7: List all teachers")
        print("8: List all grades")
        print("9: Search for a student")
        print("10: Search for a course")
        print("11: Search for a teacher")
        print("12: Search for a grade")
        print("13: Import data from CSV")
        print("0: Logout")
        choice = input("Please input a number to run the program: ").strip()
        # print(f"[DEBUG] User entered: {choice}")  # Debug information
        try:
            if choice == "1":
                DataAccess.add_student()
            elif choice == "2":
                DataAccess.add_course()
            elif choice == "3":
                DataAccess.add_teacher()
            elif choice == "4":
                DataAccess.add_grade()
            elif choice == "5":
                print("[DEBUG] Calling list_all_students...")
                DataAccess.list_all_students()
            elif choice == "6":
                print("[DEBUG] Calling list_all_courses...")
                DataAccess.list_all_courses()
            elif choice == "7":
                print("[DEBUG] Calling list_all_teachers...")
                DataAccess.list_all_teachers()
            elif choice == "8":
                print("[DEBUG] Calling list_all_grades...")
                DataAccess.list_all_grades()
            elif choice == "9":
                student_id = input("Enter student ID: ").strip()
                DataAccess.get_student_by_id(student_id)
            elif choice == "10":
                course_id = input("Enter course ID: ").strip()
                DataAccess.get_course_by_id(course_id)
            elif choice == "11":
                teacher_id = input("Enter teacher ID: ").strip()
                DataAccess.get_teacher_by_id(teacher_id)
            elif choice == "12":
                student_id = input("Enter student ID: ").strip()
                course_id = input("Enter course ID: ").strip()
                DataAccess.get_grade_and_statistics(student_id, course_id)
            elif choice == "13":
                file_path = input("Enter the path to the CSV file: ").strip()
                DataAccess.import_all_data_from_csv(file_path)
            elif choice == "0":
                print("Logging out...")
                break
            else:
                print("Invalid option. Please try again.")
        except Exception as e:
            print(f"[DEBUG] An error occurred: {e}")  # Catch all exceptions for debugging