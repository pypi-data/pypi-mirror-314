from person.person import Person
from encryption import Encryption

class Teacher(Person):
    def __init__(self, name, teacher_id, login_name, password):
        super().__init__(name=name)
        self.teacher_id = teacher_id
        self.login_name = login_name
        self.password = Encryption.encrypt(password)

    def get_password(self, s_key):
        # 安全解密逻辑
        authorized_key = "jieyiyao@student.ubc.ca" 
        return Encryption.decrypt(self.password) if s_key == authorized_key else "Incorrect key"

    def __str__(self):
        return f"Teacher ID: {self.teacher_id}, Name: {self.name}, Login: {self.login_name}"