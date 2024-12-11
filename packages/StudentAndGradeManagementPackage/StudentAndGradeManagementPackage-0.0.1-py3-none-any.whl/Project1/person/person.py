class Person:
    def __init__(self, name, gender=None):
        self.name = name
        if gender:
            gender = gender.upper()
            if gender in ["M", "MALE"]:
                self.gender = "Male"
            elif gender in ["F", "FEMALE"]:
                self.gender = "Female"
            else:
                raise ValueError("Invalid gender. Please use 'M' for Male or 'F' for Female.")
        else:
            self.gender = "Not Specified"  # 如果没有指定性别，设置为默认值

    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}"