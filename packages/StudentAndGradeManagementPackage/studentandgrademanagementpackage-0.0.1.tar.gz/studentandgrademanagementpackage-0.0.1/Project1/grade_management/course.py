class Course:
    def __init__(self, course_name, course_id):
        self.course_name = course_name
        self.course_id = course_id

    def __str__(self):
        return f"Course ID: {self.course_id}, Name: {self.course_name}"
    def add_student(self, student):

        self.students.append(student)

    def list_students(self):

        return [str(student) for student in self.students]