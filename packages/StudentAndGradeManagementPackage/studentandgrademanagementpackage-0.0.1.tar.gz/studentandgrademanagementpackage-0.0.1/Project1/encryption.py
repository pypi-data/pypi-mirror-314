from cryptography.fernet import Fernet

class Encryption:
    key = b'RJK4xtUwZzs2Z8PQsgJxI-B-87T_OFPWUhXGJuDiBms='  
    cipher_suite = Fernet(key)

    @staticmethod
    def encrypt(text):
        """Encrypt the input text."""
        return Encryption.cipher_suite.encrypt(text.encode()).decode()

    @staticmethod
    def decrypt(text):
        """Decrypt the input text."""
        if text is None:
            raise ValueError("Cannot decrypt None value") 
        return Encryption.cipher_suite.decrypt(text.encode()).decode()
