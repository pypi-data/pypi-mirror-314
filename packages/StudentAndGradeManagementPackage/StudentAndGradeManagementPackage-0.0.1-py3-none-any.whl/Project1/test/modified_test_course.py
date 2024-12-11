import unittest
from grade_management.course import Course

class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setup Class: Initializing resources for TestCourse class.")

    @classmethod
    def tearDownClass(cls):
        print("Teardown Class: Cleaning up resources for TestCourse class.")

    def setUp(self):
        self.course_name = "Python Programming"
        self.course_id = "CS101"
        self.course = Course(self.course_name, self.course_id)

    def tearDown(self):
        print("Teardown: Clean up after a test case.")

    def test_course_initialization(self):
        self.assertEqual(self.course.course_name, self.course_name, "Course name should match the initialized value.")
        self.assertEqual(self.course.course_id, self.course_id, "Course ID should match the initialized value.")
        self.assertIsInstance(self.course, Course, "Object should be an instance of Course.")

    def test_course_string_representation(self):
        expected_str = f"Course ID: {self.course_id}, Name: {self.course_name}"
        self.assertEqual(str(self.course), expected_str, "String representation should match expected format.")

if __name__ == '__main__':
    unittest.main()
