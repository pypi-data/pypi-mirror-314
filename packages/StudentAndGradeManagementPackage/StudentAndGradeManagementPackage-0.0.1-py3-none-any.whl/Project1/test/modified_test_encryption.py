import unittest
from encryption import Encryption

class TestEncryption(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setup Class: Initializing resources for TestEncryption class.")

    @classmethod
    def tearDownClass(cls):
        print("Teardown Class: Cleaning up resources for TestEncryption class.")

    def setUp(self):
        self.sample_text = "secure_password"
        self.sample_key = "jieyi.yao@student.xjtlu.edu.cn"
        self.encrypted_text = Encryption.encrypt(self.sample_text)

    def tearDown(self):
        print("Teardown: Clean up after a test case.")

    def test_encryption(self):
        self.assertNotEqual(self.sample_text, self.encrypted_text, "Encryption should produce a different output.")
        self.assertIsInstance(self.encrypted_text, str, "Encrypted output should be a string.")
        decrypted_text = Encryption.decrypt(self.encrypted_text)
        self.assertEqual(decrypted_text, self.sample_text, "Decryption should return the original text.")
        self.assertIsInstance(decrypted_text, str, "Decrypted output should be a string.")

    def test_invalid_decryption(self):
        with self.assertRaises(ValueError):
            Encryption.decrypt(None)
        self.assertNotEqual(Encryption.decrypt(self.encrypted_text), "wrong_value")

if __name__ == '__main__':
    unittest.main()
