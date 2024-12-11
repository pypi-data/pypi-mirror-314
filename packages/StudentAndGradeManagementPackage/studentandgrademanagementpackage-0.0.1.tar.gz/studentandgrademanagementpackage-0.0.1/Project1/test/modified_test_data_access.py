from data_access_analysis.data_access import DataAccess
from person.student import Student
from person.teacher import Teacher
from grade_management.course import Course
from grade_management.grade import Grade
import unittest

class TestDataAccess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setup Class: Initializing resources for TestDataAccess class.")
        cls.student = Student("Alice", "Female", "S001")
        cls.teacher = Teacher("Dr. Smith", "T001", "drsmith", "password")
        cls.course = Course("Math 101", "M101")
        cls.grade = Grade("S001", "M101", 85)

    @classmethod
    def tearDownClass(cls):
        print("Teardown Class: Cleaning up resources for TestDataAccess class.")
        DataAccess.students_list.clear()
        DataAccess.teachers_list.clear()
        DataAccess.courses_list.clear()
        DataAccess.grades_list.clear()

    def setUp(self):
        DataAccess.students_list.append(self.student)
        DataAccess.teachers_list.append(self.teacher)
        DataAccess.courses_list.append(self.course)
        DataAccess.grades_list.append(self.grade)

    def tearDown(self):
        DataAccess.students_list.clear()
        DataAccess.teachers_list.clear()
        DataAccess.courses_list.clear()
        DataAccess.grades_list.clear()

    def test_add_student(self):
        new_student = Student("Bob", "Male", "S002")
        DataAccess.students_list.append(new_student)
        self.assertIn(new_student, DataAccess.students_list, "New student should be added to the list.")
        self.assertEqual(len(DataAccess.students_list), 2, "There should be two students in the list.")

    def test_add_teacher(self):
        new_teacher = Teacher("Dr. Doe", "T002", "drdoe", "password123")
        DataAccess.teachers_list.append(new_teacher)
        self.assertIn(new_teacher, DataAccess.teachers_list, "New teacher should be added to the list.")
        self.assertEqual(len(DataAccess.teachers_list), 2, "There should be two teachers in the list.")

    def test_get_student_by_id(self):
        result = None
        for student in DataAccess.students_list:
            if student.student_id == "S001":
                result = student
        self.assertEqual(result, self.student, "Should retrieve the correct student by ID.")

    def test_get_course_by_id(self):
        result = None
        for course in DataAccess.courses_list:
            if course.course_id == "M101":
                result = course
        self.assertEqual(result, self.course, "Should retrieve the correct course by ID.")

if __name__ == '__main__':
    unittest.main()
