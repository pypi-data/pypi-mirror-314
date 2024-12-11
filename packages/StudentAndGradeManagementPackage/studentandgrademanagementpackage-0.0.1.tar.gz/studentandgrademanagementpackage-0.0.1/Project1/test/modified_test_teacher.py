import unittest
from person.teacher import Teacher
from encryption import Encryption

class TestTeacher(unittest.TestCase):
    def setUp(self):
        self.teacher = Teacher("Dr. Smith", "T001", "drsmith", "securepassword")

    def test_initialization(self):
        self.assertEqual(self.teacher.name, "Dr. Smith")
        self.assertEqual(self.teacher.teacher_id, "T001")
        self.assertEqual(self.teacher.login_name, "drsmith")

    def test_encrypted_password(self):
        encrypted_password = self.teacher.password
        self.assertNotEqual(encrypted_password, "securepassword")
        self.assertTrue(Encryption.decrypt(encrypted_password), "securepassword")

    def test_get_password_correct_key(self):
        correct_password = self.teacher.get_password("jieyiyao@student.ubc.ca")
        self.assertEqual(correct_password, "securepassword")

    def test_get_password_incorrect_key(self):
        wrong_password = self.teacher.get_password("wrong_key")
        self.assertEqual(wrong_password, "Incorrect key")

    def test_string_representation(self):
        self.assertEqual(
            str(self.teacher),
            "Teacher ID: T001, Name: Dr. Smith, Login: drsmith"
        )

if __name__ == "__main__":
    unittest.main()