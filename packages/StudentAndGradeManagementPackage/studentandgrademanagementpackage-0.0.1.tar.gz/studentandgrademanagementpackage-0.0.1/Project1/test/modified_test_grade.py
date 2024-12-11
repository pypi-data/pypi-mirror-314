from grade_management.grade import Grade
import unittest

class TestGrade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setup Class: Initializing resources for TestGrade class.")

    @classmethod
    def tearDownClass(cls):
        print("Teardown Class: Cleaning up resources for TestGrade class.")

    def setUp(self):
        self.student_id = "S001"
        self.course_id = "CS101"
        self.grade_value = 95.5
        self.grade = Grade(self.student_id, self.course_id, self.grade_value)

    def tearDown(self):
        print("Teardown: Clean up after a test case.")

    def test_grade_initialization(self):
        self.assertEqual(self.grade.student_id, self.student_id, "Student ID should match the initialized value.")
        self.assertEqual(self.grade.course_id, self.course_id, "Course ID should match the initialized value.")
        self.assertEqual(self.grade.grade_value, self.grade_value, "Grade value should match the initialized value.")
        self.assertIsInstance(self.grade, Grade, "Object should be an instance of Grade.")

    def test_grade_string_representation(self):
        expected_str = f"Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade_value}"
        self.assertEqual(str(self.grade), expected_str, "String representation should match expected format.")

if __name__ == '__main__':
    unittest.main()
