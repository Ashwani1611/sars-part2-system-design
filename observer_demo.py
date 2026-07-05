# task 2.3d - observer pattern, admin panel notifies email + audit log when marks get updated

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, student_id, new_marks):
        pass


class MarksUpdateNotifier:
    # this is the subject, admin panel calls notify() on this whenever marks change
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def deregister(self, observer):
        self._observers.remove(observer)

    def notify(self, student_id, new_marks):
        for observer in self._observers:
            observer.update(student_id, new_marks)


class EmailNotifier(Observer):
    def update(self, student_id, new_marks):
        print(f"[Email] telling student {student_id}: new marks = {new_marks}")


class AuditLogNotifier(Observer):
    def update(self, student_id, new_marks):
        print(f"[AuditLog] logged: student {student_id} marks changed to {new_marks}")


if __name__ == "__main__":
    notifier = MarksUpdateNotifier()

    email_obs = EmailNotifier()
    audit_obs = AuditLogNotifier()

    notifier.register(email_obs)
    notifier.register(audit_obs)

    # admin updates marks, both observers get notified
    notifier.notify(student_id=101, new_marks=88.5)

    # now deregister email notifier and update marks again
    notifier.deregister(email_obs)
    print("---after deregistering email notifier---")
    notifier.notify(student_id=101, new_marks=91.0)