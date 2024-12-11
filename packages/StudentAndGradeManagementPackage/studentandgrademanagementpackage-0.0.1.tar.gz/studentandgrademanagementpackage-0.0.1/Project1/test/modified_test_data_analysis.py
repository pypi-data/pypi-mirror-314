import unittest
from unittest.mock import patch
from data_access_analysis.data_access import DataAccess
from grade_management.grade import Grade
from data_access_analysis.data_analysis import DataAnalysis


class TestDataAnalysis(unittest.TestCase):
    def setUp(self):
        # Clear grades_list before each test
        DataAccess.grades_list = []

    def test_display_average_grade_with_grades(self):
        """Test display_average_grade with valid grades."""
        # Add test data
        DataAccess.grades_list = [
            Grade(student_id="S001", course_id="C001", grade_value=85.0),
            Grade(student_id="S002", course_id="C001", grade_value=95.0)
        ]
        expected_average = (85.0 + 95.0) / 2  # Calculate the expected average

        # Capture output and assert
        with patch("builtins.print") as mock_print:
            DataAnalysis.display_average_grade("C001")
            mock_print.assert_called_with(f"Average grade for Course ID C001 is {expected_average:.2f}.")

    def test_display_average_grade_no_grades(self):
        """Test display_average_grade when no grades are available."""
        # Capture output when there are no grades
        with patch("builtins.print") as mock_print:
            DataAnalysis.display_average_grade("C002")
            mock_print.assert_called_with("No grades available for Course ID C002.")

    def test_convert_grades_to_gpa_with_grades(self):
        """Test convert_grades_to_gpa with valid grades."""
        # Add test data
        DataAccess.grades_list = [
            Grade(student_id="S001", course_id="C001", grade_value=85.0),
            Grade(student_id="S001", course_id="C002", grade_value=75.0)
        ]
        # Expected GPA calculation
        expected_gpa = (3.0 + 2.0) / 2

        # Capture output and assert
        with patch("builtins.print") as mock_print:
            DataAnalysis.convert_grades_to_gpa("S001")
            mock_print.assert_called_with(f"GPA for Student ID S001: {expected_gpa:.2f}")

    def test_convert_grades_to_gpa_no_grades(self):
        """Test convert_grades_to_gpa when no grades are available."""
        # Capture output when there are no grades
        with patch("builtins.print") as mock_print:
            DataAnalysis.convert_grades_to_gpa("S002")
            mock_print.assert_called_with("No grades found for Student ID S002.")


if __name__ == "__main__":
    unittest.main()