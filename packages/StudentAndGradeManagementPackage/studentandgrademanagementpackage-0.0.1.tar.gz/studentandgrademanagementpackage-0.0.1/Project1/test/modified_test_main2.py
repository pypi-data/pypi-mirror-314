import unittest
from unittest.mock import patch, mock_open
from grade_management.grade import Grade
from menu import grade_analysis_menu
from menu import teacher_menu 
import pandas as pd
import csv

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from data_access_analysis.data_access import DataAccess
from data_access_analysis.data_analysis import DataAnalysis
from encryption import Encryption
from grade_management.course import Course
from grade_management.grade import Grade
from person.student import Student
from person.teacher import Teacher



class TestGradeAnalysisMenu(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "0"])  # Simulate selecting option 1 and then exiting
    @patch("data_access_analysis.data_analysis.DataAnalysis.display_average_grade")  # Mock display_average_grade
    def test_display_average_grade(self, mock_display, mock_input):
        """
        Test the display_average_grade option in grade_analysis_menu.
        """
        mock_display.return_value = None  # Simulate function execution
        grade_analysis_menu("S001")  # Assume student_id "S001"

        # Verify that the display_average_grade method was called with the correct student_id
        mock_display.assert_called_once_with("S001")

    @patch("builtins.input", side_effect=["2", "0"])  # Simulate selecting option 2 and then exiting
    @patch("data_access_analysis.data_analysis.DataAnalysis.convert_grades_to_gpa")  # Mock convert_grades_to_gpa
    def test_convert_grades_to_gpa(self, mock_convert, mock_input):
        """
        Test the convert_grades_to_gpa option in grade_analysis_menu.
        """
        mock_convert.return_value = None  # Simulate function execution
        grade_analysis_menu("S001")  # Assume student_id "S001"

        # Verify that the convert_grades_to_gpa method was called with the correct student_id
        mock_convert.assert_called_once_with("S001")

    @patch("builtins.input", side_effect=["3", "C001", "0"])  # Simulate selecting option 3, entering course ID, and then exiting
    @patch("data_access_analysis.data_access.DataAccess.get_statistics")  # Mock get_statistics
    def test_analyze_specific_course(self, mock_get_stats, mock_input):
        """
        Test the analyze grades for a specific course option in grade_analysis_menu.
        """
        mock_get_stats.return_value = None  # Simulate function execution
        grade_analysis_menu("S001")  # Assume student_id "S001"

        # Verify that the get_statistics method was called with the correct course_id
        mock_get_stats.assert_called_once_with("C001")

    @patch("builtins.input", side_effect=["0"])  # Simulate selecting the exit option
    @patch("builtins.print")  # Mock print to verify output
    def test_menu_exit(self, mock_print, mock_input):
        """
        Test exiting the grade_analysis_menu.
        """
        grade_analysis_menu("S001")  # Assume student_id "S001"

        # Verify the correct print message
        mock_print.assert_any_call("Returning to Student Menu...")
            
class TestTeacherMenu(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        # Example data setup can go here if needed (e.g., setting up mock data)
        DataAccess.students_list = []
        DataAccess.courses_list = []
        DataAccess.teachers_list = []
        DataAccess.grades_list = []
    
    def setUp(self):
        """Set up before each test."""
        # Clear previous lists before each test
        DataAccess.students_list.clear()
        DataAccess.courses_list.clear()
        DataAccess.teachers_list.clear()
        DataAccess.grades_list.clear()

    @patch("builtins.input", side_effect=["1", "0"])  # Mocking input for adding a student and logging out
    @patch("builtins.print")  # Mocking print to capture output
    def test_add_student(self, mock_print, mock_input):
        """Test adding a student."""
        with patch.object(DataAccess, 'add_student', return_value=None) as mock_add_student:
            teacher_menu()  # Call the menu function
            mock_add_student.assert_called_once()  # Ensure add_student is called once
            mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

    @patch("builtins.input", side_effect=["2", "0"])  # Mocking input for adding a course and logging out
    @patch("builtins.print")
    def test_add_course(self, mock_print, mock_input):
        """Test adding a course."""
        with patch.object(DataAccess, 'add_course', return_value=None) as mock_add_course:
            teacher_menu()  # Call the menu function
            mock_add_course.assert_called_once()  # Ensure add_course is called once
            mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

    @patch("builtins.input", side_effect=["3", "0"])  # Mocking input for adding a teacher and logging out
    @patch("builtins.print")
    def test_add_teacher(self, mock_print, mock_input):
        """Test adding a teacher."""
        with patch.object(DataAccess, 'add_teacher', return_value=None) as mock_add_teacher:
            teacher_menu()  # Call the menu function
            mock_add_teacher.assert_called_once()  # Ensure add_teacher is called once
            mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

    @patch("builtins.input", side_effect=["4", "0"])  # Mocking input for adding a grade and logging out
    @patch("builtins.print")
    def test_add_grade(self, mock_print, mock_input):
        """Test adding a grade."""
        with patch.object(DataAccess, 'add_grade', return_value=None) as mock_add_grade:
            teacher_menu()  # Call the menu function
            mock_add_grade.assert_called_once()  # Ensure add_grade is called once
            mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

    @patch("builtins.input", side_effect=["5", "0"])  # Mocking input for listing students and logging out
    @patch("builtins.print")
    def test_list_all_students(self, mock_print, mock_input):
        """Test listing all students."""
        with patch.object(DataAccess, 'list_all_students', return_value=None) as mock_list_all_students:
            teacher_menu()  # Call the menu function
            mock_list_all_students.assert_called_once()  # Ensure list_all_students is called once
            mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

    @patch("data_access_analysis.data_access.DataAccess.import_all_data_from_csv")
    @patch("builtins.input", side_effect=["13", "/path/to/mock/file.csv", "0"])
    def test_import_data_from_csv(self, mock_input, mock_import):
        """Test importing data from CSV in teacher_menu."""
        mock_import.return_value = None  # Mock the import method
        teacher_menu()  # Call the menu function
        mock_import.assert_called_once_with("/path/to/mock/file.csv")

    @patch("builtins.input", side_effect=["0"])  # Mocking input for logging out
    @patch("builtins.print")
    def test_logout(self, mock_print, mock_input):
        """Test logging out."""
        teacher_menu()  # Call the menu function
        mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

    @patch("builtins.input", side_effect=["99", "0"])  # Mocking invalid input and then logging out
    @patch("builtins.print")
    def test_invalid_option(self, mock_print, mock_input):
        """Test invalid option in menu."""
        teacher_menu()  # Call the menu function
        mock_print.assert_any_call("Invalid option. Please try again.")  # Check if the invalid option message is printed
        mock_print.assert_called_with("Logging out...")  # Check if the logout message is printed

class TestImportUserCredentials(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="ID,Name,Password,Role\n1,JohnDoe,1234,Admin\n2,JaneDoe,abcd,User")
    @patch("data_access_analysis.data_access.Encryption.encrypt")
    def test_import_user_credentials_success(self, mock_encrypt, mock_file):
        """
        Test the import_user_credentials method for successful import.
        """
        mock_encrypt.side_effect = lambda x: f"encrypted_{x}"  # Mock encryption logic
        DataAccess.user_credentials = {}  # Reset the user_credentials dictionary

        DataAccess.import_user_credentials("fake_path.csv")

        # Check if the user_credentials dictionary was populated correctly
        self.assertIn("1", DataAccess.user_credentials)
        self.assertIn("2", DataAccess.user_credentials)
        self.assertEqual(DataAccess.user_credentials["1"]["name"], "JohnDoe")
        self.assertEqual(DataAccess.user_credentials["1"]["password"], "encrypted_1234")
        self.assertEqual(DataAccess.user_credentials["1"]["role"], "Admin")
        self.assertEqual(DataAccess.user_credentials["2"]["name"], "JaneDoe")
        self.assertEqual(DataAccess.user_credentials["2"]["password"], "encrypted_abcd")
        self.assertEqual(DataAccess.user_credentials["2"]["role"], "User")

        # Verify the file was opened with the correct path
        mock_file.assert_called_once_with("fake_path.csv", mode='r', newline='', encoding='utf-8')

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_import_user_credentials_file_not_found(self, mock_file):
        """
        Test the import_user_credentials method for FileNotFoundError.
        """
        with patch("builtins.print") as mock_print:
            DataAccess.import_user_credentials("non_existent_file.csv")
            mock_print.assert_called_once_with("File not found: non_existent_file.csv")

    @patch("builtins.open", new_callable=mock_open, read_data="ID,Name,Password,Role\n1,JohnDoe,1234,Admin")
    @patch("data_access_analysis.data_access.Encryption.encrypt")
    def test_import_user_credentials_error_handling(self, mock_encrypt, mock_file):
        """
        Test the import_user_credentials method for general exception handling.
        """
        mock_encrypt.side_effect = Exception("Encryption error")  # Simulate an exception during encryption

        with patch("builtins.print") as mock_print:
            DataAccess.import_user_credentials("fake_path.csv")
            mock_print.assert_called_with("Error occurred during import: Encryption error")

class TestDataAccessListingAndRetrieval(unittest.TestCase):
    def setUp(self):
        # Clear DataAccess lists before each test
        DataAccess.students_list = []
        DataAccess.teachers_list = []
        DataAccess.courses_list = []
        DataAccess.grades_list = []

    # Tests for listing all entities
    def test_list_all_students_empty(self):
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_students()
            mock_print.assert_called_with("No students found.")

    def test_list_all_students_with_data(self):
        DataAccess.students_list = [Student(name="Alice", gender="Female", student_id="S001")]
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_students()
            mock_print.assert_called_with(DataAccess.students_list[0])

    def test_list_all_teachers_empty(self):
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_teachers()
            mock_print.assert_called_with("No teachers found.")

    def test_list_all_teachers_with_data(self):
        DataAccess.teachers_list = [Teacher(name="Dr. Smith", teacher_id="T001", login_name="drsmith", password="password")]
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_teachers()
            mock_print.assert_called_with(DataAccess.teachers_list[0])

    def test_list_all_courses_empty(self):
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_courses()
            mock_print.assert_called_with("No courses found.")

    def test_list_all_courses_with_data(self):
        DataAccess.courses_list = [Course(course_name="Math 101", course_id="C001")]
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_courses()
            mock_print.assert_called_with(DataAccess.courses_list[0])

    def test_list_all_grades_empty(self):
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_grades()
            mock_print.assert_called_with("No grades found.")

    def test_list_all_grades_with_data(self):
        DataAccess.grades_list = [Grade(student_id="S001", course_id="C001", grade_value=85.0)]
        with patch("builtins.print") as mock_print:
            DataAccess.list_all_grades()
            mock_print.assert_called_with(DataAccess.grades_list[0])

    # Tests for retrieval by ID
    def test_get_student_by_id_found(self):
        DataAccess.students_list = [Student(name="Alice", gender="Female", student_id="S001")]
        with patch("builtins.print") as mock_print:
            DataAccess.get_student_by_id("S001")
            mock_print.assert_called_with(DataAccess.students_list[0])

    def test_get_student_by_id_not_found(self):
        with patch("builtins.print") as mock_print:
            DataAccess.get_student_by_id("S002")
            mock_print.assert_called_with("Student not found.")

    def test_get_teacher_by_id_found(self):
        DataAccess.teachers_list = [Teacher(name="Dr. Smith", teacher_id="T001", login_name="drsmith", password="password")]
        with patch("builtins.print") as mock_print:
            DataAccess.get_teacher_by_id("T001")
            mock_print.assert_called_with(DataAccess.teachers_list[0])

    def test_get_teacher_by_id_not_found(self):
        with patch("builtins.print") as mock_print:
            DataAccess.get_teacher_by_id("T002")
            mock_print.assert_called_with("Teacher not found.")

    def test_get_course_by_id_found(self):
        DataAccess.courses_list = [Course(course_name="Math 101", course_id="C001")]
        with patch("builtins.print") as mock_print:
            DataAccess.get_course_by_id("C001")
            mock_print.assert_called_with(DataAccess.courses_list[0])

    def test_get_course_by_id_not_found(self):
        with patch("builtins.print") as mock_print:
            DataAccess.get_course_by_id("C002")
            mock_print.assert_called_with("Course not found.")

    def test_get_grade_by_student_and_course_found(self):
        DataAccess.grades_list = [Grade(student_id="S001", course_id="C001", grade_value=85.0)]
        with patch("builtins.print") as mock_print:
            DataAccess.get_grade_by_student_and_course("S001", "C001")
            mock_print.assert_called_with(f"Grade found: {DataAccess.grades_list[0]}")

    def test_get_grade_by_student_and_course_not_found(self):
        with patch("builtins.print") as mock_print:
            DataAccess.get_grade_by_student_and_course("S001", "C002")
            mock_print.assert_called_with("No grade found for the given student ID and course ID.")

    def test_get_grades_by_student_id_found(self):
        DataAccess.grades_list = [Grade(student_id="S001", course_id="C001", grade_value=85.0)]
        with patch("builtins.print") as mock_print:
            DataAccess.get_grades_by_student_id("S001")
            mock_print.assert_called_with(DataAccess.grades_list[0])

    def test_get_grades_by_student_id_not_found(self):
        with patch("builtins.print") as mock_print:
            DataAccess.get_grades_by_student_id("S002")
            mock_print.assert_called_with("No grades found for the student with ID: S002.")
class TestDataAccessCSVImport(unittest.TestCase):
    def setUp(self):
        # Clear all data lists before each test
        DataAccess.students_list = []
        DataAccess.teachers_list = []
        DataAccess.courses_list = []
        DataAccess.grades_list = []

    @patch("builtins.open", new_callable=mock_open, read_data="""Student_ID,Student_Name,Gender,Course_ID,Course_Name,Grade_Value,Teacher_ID,Teacher_Name
S001,Alice,Female,C001,Math 101,85.0,T001,Dr. Smith
S002,Bob,Male,C002,Science 101,90.0,T002,Dr. Johnson""")
    def test_import_all_data_from_csv(self, mock_file):
        """Test importing data from a CSV file."""
        file_path = "mock_data.csv"
        DataAccess.import_all_data_from_csv(file_path)

        # Verify students were added
        self.assertEqual(len(DataAccess.students_list), 2)
        self.assertEqual(DataAccess.students_list[0].name, "Alice")
        self.assertEqual(DataAccess.students_list[1].gender, "Male")

        # Verify teachers were added
        self.assertEqual(len(DataAccess.teachers_list), 2)
        self.assertEqual(DataAccess.teachers_list[0].name, "Dr. Smith")

        # Verify courses were added
        self.assertEqual(len(DataAccess.courses_list), 2)
        self.assertEqual(DataAccess.courses_list[0].course_name, "Math 101")

        # Verify grades were added
        self.assertEqual(len(DataAccess.grades_list), 2)
        self.assertEqual(DataAccess.grades_list[0].grade_value, 85.0)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_import_csv_file_not_found(self, mock_file):
        """Test importing from a non-existent CSV file."""
        file_path = "non_existent_file.csv"
        with patch("builtins.print") as mock_print:
            DataAccess.import_all_data_from_csv(file_path)
            mock_print.assert_called_with(f"File not found: {file_path}")


class TestGradeStatistics(unittest.TestCase):
    def setUp(self):
        # Clear grades list before each test
        DataAccess.grades_list = []

    def test_get_statistics_with_grades(self):
        """Test retrieving statistics for a course with grades."""
        DataAccess.grades_list = [
            Grade(student_id="S001", course_id="C001", grade_value=85.0),
            Grade(student_id="S002", course_id="C001", grade_value=95.0),
        ]
        with patch("matplotlib.pyplot.show"):
            with patch("builtins.print") as mock_print:
                DataAccess.get_statistics("C001")
                # Use robust assertion
                self.assertTrue(
                    any("Statistics for Course ID C001:" in str(call) for call in mock_print.call_args_list),
                    "Expected statistics output not found."
                )

    def test_get_statistics_no_grades(self):
        """Test retrieving statistics for a course with no grades."""
        with patch("builtins.print") as mock_print:
            DataAccess.get_statistics("C002")
            mock_print.assert_called_with("No grades available for Course ID C002.")

    def test_get_grade_and_statistics_found(self):
        """Test retrieving a specific grade and course statistics."""
        DataAccess.grades_list = [
            Grade(student_id="S001", course_id="C001", grade_value=85.0),
            Grade(student_id="S002", course_id="C001", grade_value=95.0),
        ]
        with patch("matplotlib.pyplot.show"):
            with patch("builtins.print") as mock_print:
                DataAccess.get_grade_and_statistics("S001", "C001")
                mock_print.assert_any_call("Found Grade: Student ID S001, Course ID C001, Grade 85.0")

    def test_get_grade_and_statistics_not_found(self):
        """Test retrieving a grade that does not exist."""
        DataAccess.grades_list = [
            Grade(student_id="S001", course_id="C001", grade_value=85.0),
        ]
        with patch("builtins.print") as mock_print:
            DataAccess.get_grade_and_statistics("S002", "C002")
            mock_print.assert_called_with("No grade found for Student ID: S002 and Course ID: C002.")


if __name__ == "__main__":
    unittest.main()