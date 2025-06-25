class Person:
    def __init__(self, name):
        self.__name = name  # đóng gói

    def get_name(self):
        return self.__name

    def introduce(self):  # đa hình
        print(f"My name is {self.__name}")

class Student(Person):  # kế thừa
    def __init__(self, name, student_id):
        super().__init__(name)
        self.student_id = student_id

    def introduce(self):  # ghi đè (override)
        print(f"Im a student, my ID is {self.student_id}")
person = Person('Alice')
person.introduce()
student = Student('Bob','sv12345')
student.introduce()
