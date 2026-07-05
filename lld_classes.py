# task 2.3 - student, enrollment classes + enrollment repo interface

from abc import ABC, abstractmethod


class Student:
    # no email/notification stuff in here on purpose, thats not this class's job - single responsibility
    def __init__(self, student_id, name, department, advisor_name):
        self.student_id = student_id
        self.name = name
        self.department = department
        self.advisor_name = advisor_name

    def get_profile(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "advisor_name": self.advisor_name,
        }

    def update_department(self, new_department):
        self.department = new_department


class EnrollmentRepository(ABC):
    # interface Enrollment talks to for saving/loading, doesnt care what db is actually behind it - dependency inversion
    @abstractmethod
    def save(self, enrollment):
        pass

    @abstractmethod
    def find_by_student(self, student_id):
        pass

    @abstractmethod
    def delete(self, student_id, course_code):
        pass


class Enrollment:
    # can extend this later (see below) without touching this class - open/closed principle
    def __init__(self, student_id, course_code, enrollment_year,
                 marks_obtained=None, repository=None):
        self.student_id = student_id
        self.course_code = course_code
        self.enrollment_year = enrollment_year
        self.marks_obtained = marks_obtained
        self._repository = repository

    def record_marks(self, marks):
        self.marks_obtained = marks
        if self._repository:
            self._repository.save(self)

    def status(self):
        return "enrolled"


class WaitlistedEnrollment(Enrollment):
    # extending Enrollment without changing the original - open/closed again
    def __init__(self, student_id, course_code, enrollment_year,
                 waitlist_position, repository=None):
        super().__init__(student_id, course_code, enrollment_year,
                          repository=repository)
        self.waitlist_position = waitlist_position

    def status(self):
        return f"waitlisted (position {self.waitlist_position})"