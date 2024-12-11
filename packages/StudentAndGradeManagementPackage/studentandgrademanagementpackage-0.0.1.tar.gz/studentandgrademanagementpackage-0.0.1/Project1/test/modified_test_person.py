from person.person import Person
import unittest

class TestPerson(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setup Class: Initializing resources for TestPerson class.")

    @classmethod
    def tearDownClass(cls):
        print("Teardown Class: Cleaning up resources for TestPerson class.")

    def setUp(self):
        self.name = "Alice"
        self.gender = "Female"
        self.person = Person(self.name, self.gender)

    def tearDown(self):
        print("Teardown: Clean up after a test case.")

    def test_person_initialization(self):
        self.assertEqual(self.person.name, self.name, "Name should match the initialized value.")
        self.assertEqual(self.person.gender, self.gender, "Gender should match the initialized value.")
        self.assertIsInstance(self.person, Person, "Object should be an instance of Person.")

    def test_person_string_representation(self):
        expected_str = f"Name: {self.name}, Gender: {self.gender}"
        self.assertEqual(str(self.person), expected_str, "String representation should match expected format.")

if __name__ == '__main__':
    unittest.main()
