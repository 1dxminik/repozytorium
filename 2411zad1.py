class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def is_passed(self):
        srednia = sum(self.marks) / len(self.marks)

        return srednia > 50


Student1 = Student("Dominik", [100, 100, 100])
Student2 = Student("Piotrek", [67, 67, 67])
Student3 = Student("Mohammed", [20, 0, 10])

print(Student1.is_passed())
print(Student2.is_passed())
print(Student3.is_passed())
