
class Grade:
    def __init__(self, student_id, course_id, grade_value):
        self.student_id = student_id
        self.course_id = course_id
        self.grade_value = grade_value

    def __str__(self):
        return f"Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade_value}"

