from person.person import Person

class Student(Person):
    def __init__(self, name="Unknown", gender="Unknown", student_id=None):
        super().__init__(name, gender)
        self.student_id = student_id
        self.courses = []  # Stores the courses the student has registered for

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.name}, Gender: {self.gender}"

    def enroll_course(self, course):
        """Enroll in a course"""
        self.courses.append(course)

    def list_courses(self):
        """List all courses the student has registered for"""
        return [str(course) for course in self.courses]