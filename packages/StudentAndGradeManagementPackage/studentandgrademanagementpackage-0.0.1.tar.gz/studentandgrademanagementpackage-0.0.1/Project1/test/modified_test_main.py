import unittest
from unittest.mock import patch
from menu import login, student_menu, teacher_menu
from data_access_analysis.data_access import DataAccess
from encryption import Encryption
from data_access_analysis.data_analysis import DataAnalysis
from person.student import Student
from person.teacher import Teacher

class TestGradeAnalysisMenu(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setup Class: Initializing resources for TestGradeAnalysisMenu class.")

    def setUp(self):
        DataAccess.students_list.clear()

    def tearDown(self):
        DataAccess.students_list.clear()

    def test_add_new_student(self):
        """Test adding a new student."""
        with patch("builtins.input", side_effect=["S002", "Bob", "M", "-1"]):
            DataAccess.add_student()
        self.assertEqual(len(DataAccess.students_list), 1, "There should be one student in the list.")
        self.assertEqual(DataAccess.students_list[0].student_id, "S002", "The student ID should match.")
        self.assertEqual(DataAccess.students_list[0].gender, "Male", "The student gender should match.")

    def test_add_student_with_existing_id_but_not_overwrite(self):
        """Test adding a student with an existing ID but choosing not to overwrite."""
        student = Student("Alice", "Female", "S001")
        DataAccess.students_list.append(student)
        with patch("builtins.input", side_effect=["S001", "Bob", "M", "n", "-1"]):
            DataAccess.add_student()
        self.assertEqual(len(DataAccess.students_list), 1, "There should still be one student in the list.")
        self.assertEqual(DataAccess.students_list[0].name, "Alice", "The original student name should remain.")
        self.assertEqual(DataAccess.students_list[0].gender, "Female", "The original student gender should remain.")

    def test_update_existing_student(self):
        """Test updating an existing student."""
        student = Student("Alice", "Female", "S001")
        DataAccess.students_list.append(student)
        with patch("builtins.input", side_effect=["S001", "Bob", "M", "y", "-1"]):
            DataAccess.add_student()
        self.assertEqual(len(DataAccess.students_list), 1, "There should still be one student in the list.")
        self.assertEqual(DataAccess.students_list[0].name, "Bob", "The student name should be updated.")
        self.assertEqual(DataAccess.students_list[0].gender, "Male", "The student gender should be updated.")

    def test_add_duplicate_student_without_conflict(self):
        """Test adding two students with unique IDs."""
        with patch("builtins.input", side_effect=["S001", "Alice", "F", "-1", "S002", "Bob", "M", "-1"]):
            DataAccess.add_student()
            DataAccess.add_student()
        self.assertEqual(len(DataAccess.students_list), 2, "There should be two students in the list.")
        self.assertEqual(DataAccess.students_list[0].student_id, "S001", "The first student ID should match.")
        self.assertEqual(DataAccess.students_list[1].student_id, "S002", "The second student ID should match.")




class TestMainMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up default encrypted credentials for testing."""
        # Encrypt passwords for default user credentials
        encrypted_student_password = Encryption.encrypt("1")  # Encrypt "1" for student
        encrypted_teacher_password = Encryption.encrypt("1")  # Encrypt "1" for teacher

        # Set default user credentials
        DataAccess.user_credentials["S001"] = {
            "name": "Default Student",
            "password": encrypted_student_password,  # Use encrypted password
            "role": "Student",
        }
        DataAccess.user_credentials["T001"] = {
            "name": "Default Teacher",
            "password": encrypted_teacher_password,  # Use encrypted password
            "role": "Teacher",
        }

    def test_main_menu_student_login_default(self):
        """Test default student login."""
        with patch("builtins.input", side_effect=["1", "S001", "1", "0"]):  # Simulate student login
            with patch("menu.student_menu") as mock_student_menu:
                login()
                mock_student_menu.assert_called_once_with("S001")

    def test_main_menu_teacher_login_default(self):
        """Test default teacher login."""
        with patch("builtins.input", side_effect=["2", "T001", "1", "0"]):  # Simulate teacher login
            with patch("menu.teacher_menu") as mock_teacher_menu:
                login()
                mock_teacher_menu.assert_called_once()

    def test_invalid_option_in_main_menu(self):
        """Test invalid option in the main menu."""
        with patch("builtins.input", side_effect=["5", "0"]):  # Simulate invalid option
            with patch("builtins.print") as mock_print:
                login()
                mock_print.assert_any_call("Invalid option. Please try again.")

    def test_student_menu_view_grades(self):
        """Test student menu's 'view grades' option."""
        with patch("builtins.input", side_effect=["2", "0"]):
            with patch("data_access_analysis.data_access.DataAccess.get_grades_by_student_id") as mock_view_grades:
                student_menu("S001")
                mock_view_grades.assert_called_once_with("S001")

    def test_teacher_menu_add_grade(self):
        """Test teacher menu's 'add grade' option."""
        with patch("builtins.input", side_effect=["4", "S001", "M101", "95", "0"]):
            with patch("data_access_analysis.data_access.DataAccess.add_grade") as mock_add_grade:
                teacher_menu()
                mock_add_grade.assert_called_once()

    def test_teacher_menu_list_all_grades(self):
        """Test teacher menu's 'list all grades' option."""
        with patch("builtins.input", side_effect=["8", "0"]):
            with patch("data_access_analysis.data_access.DataAccess.list_all_grades") as mock_list_grades:
                teacher_menu()
                mock_list_grades.assert_called_once()

    def test_validate_student_success(self):
        DataAccess.user_credentials["S002"] = {"name": "Test Student", "password": "encrypted_password", "role": "Student"}
        with patch("encryption.Encryption.decrypt", return_value="1"):
            result = DataAccess.validate_student("S002", "1")
            self.assertTrue(result)

    def test_validate_student_failure(self):
        with patch("encryption.Encryption.decrypt", return_value="wrong_password"):
            result = DataAccess.validate_student("S002", "1")
            self.assertFalse(result)


    def test_student_login_flow(self):
        """Test the full student login and menu flow"""
        with patch("builtins.input", side_effect=["1", "S001", "1", "0"]):  # Student login
            with patch("menu.student_menu") as mock_student_menu:
                login()
                mock_student_menu.assert_called_once_with("S001")

    def test_teacher_login_flow(self):
        """Test the full teacher login and menu flow"""
        with patch("builtins.input", side_effect=["2", "T001", "1", "0"]):  # Teacher login
            with patch("menu.teacher_menu") as mock_teacher_menu:
                login()
                mock_teacher_menu.assert_called_once()

    def test_invalid_student_login(self):
        """Test login failure for a student with wrong credentials"""
        with patch("builtins.input", side_effect=["1", "S999", "wrongpassword", "0"]):  # Invalid student
            with patch("menu.student_menu") as mock_student_menu:
                login()
                mock_student_menu.assert_not_called()

    def test_invalid_teacher_login(self):
        """Test login failure for a teacher with wrong credentials"""
        with patch("builtins.input", side_effect=["2", "T999", "wrongpassword", "0"]):  # Invalid teacher
            with patch("menu.teacher_menu") as mock_teacher_menu:
                login()
                mock_teacher_menu.assert_not_called()

    def test_student_menu_view_information(self):
        """Test student viewing their own information"""
        DataAccess.students_list.append({"student_id": "S001", "name": "Test Student", "gender": "Female"})
        with patch("builtins.input", side_effect=["1", "0"]):  # Option 1: View my information
            with patch("data_access_analysis.data_access.DataAccess.get_student_by_id") as mock_get_info:
                student_menu("S001")
                mock_get_info.assert_called_once_with("S001")

    def test_teacher_menu_list_grades(self):
        """Test teacher listing all grades"""
        with patch("builtins.input", side_effect=["8", "0"]):  # Option 8: List all grades
            with patch("data_access_analysis.data_access.DataAccess.list_all_grades") as mock_list_grades:
                teacher_menu()
                mock_list_grades.assert_called_once()

    def test_teacher_menu_add_course(self):
        """Test teacher adding a course"""
        with patch("builtins.input", side_effect=["2", "C001", "Math 101", "0"]):  # Add a course
            with patch("data_access_analysis.data_access.DataAccess.add_course") as mock_add_course:
                teacher_menu()
                mock_add_course.assert_called_once()
                
class TestAddTeacher(unittest.TestCase):
    def setUp(self):
        DataAccess.teachers_list = []

    def test_add_new_teacher(self):
        with patch("builtins.input", side_effect=["T001", "Dr. Smith", "drsmith", "password", "-1"]):
            DataAccess.add_teacher()
        self.assertEqual(len(DataAccess.teachers_list), 1)
        self.assertEqual(DataAccess.teachers_list[0].name, "Dr. Smith")

    def test_add_existing_teacher_and_overwrite(self):
        teacher = Teacher(name="Dr. Smith", teacher_id="T001", login_name="drsmith", password="password")
        DataAccess.teachers_list.append(teacher)

        with patch("builtins.input", side_effect=["T001", "Dr. Jones", "drjones", "newpassword", "y", "-1"]):
            DataAccess.add_teacher()

        self.assertEqual(len(DataAccess.teachers_list), 1)
        self.assertEqual(DataAccess.teachers_list[0].name, "Dr. Jones")

    def test_add_teacher_with_invalid_id(self):
        with patch("builtins.input", side_effect=["", "Dr. Smith", "drsmith", "password", "-1"]), \
             patch("builtins.print") as mock_print:
            DataAccess.add_teacher()
            mock_print.assert_any_call("[DEBUG] Invalid teacher ID.")

    def test_add_teacher_with_missing_name(self):
        with patch("builtins.input", side_effect=["T002", "", "drsmith", "password", "-1"]), \
             patch("builtins.print") as mock_print:
            DataAccess.add_teacher()
            mock_print.assert_any_call("[DEBUG] Teacher name cannot be empty.")

            
if __name__ == "__main__":
    unittest.main()