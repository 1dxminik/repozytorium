class Library:
    def __init__(self, city, street, zip_code, open_hours: str, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self):
        return (f'{self.city} {self.street} {self.zip_code} {self.open_hours} '
                f'{self.phone}')


class Employee:
    def __init__(self, first_name, last_name, hire_date, birth_date, city,
                 street, zip_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self):
        return (f'{self.first_name} {self.last_name} {self.hire_date} '
                f'{self.birth_date} '
                f'{self.city} {self.street} {self.zip_code} {self.phone}')


class Book:
    def __init__(self, library, publication_date, author_name,
                 author_surname, number_of_pages):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self):
        return (f'{self.library} {self.publication_date} {self.author_name} '
                f'{self.author_surname} {self.number_of_pages}')


class Student():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')


class Order:
    def __init__(self, employee, student, books, order_date):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self):
        lista_ksiazek_tekst = ""
        for book in self.books:
            lista_ksiazek_tekst += f"\n    * {book}"

        return (f"Data: {self.order_date}\n"
                f"Pracownik: {self.employee}\n"
                f"Student: {self.student}\n"
                f"Pozycje: {lista_ksiazek_tekst}\n")


lib1 = Library("Warszawa", "Marszałkowska 1", "00-001",
               "8-16", "111-222-333")
lib2 = Library("Kraków", "Floriańska 10", "30-001",
               "10-18", "444-555-666")


emp1 = Employee("Jan", "Kowalski", "2020-01-01",
                "1990-05-05", "Warszawa", "Polna",
                "00-002", "999-999")
emp2 = Employee("Anna", "Nowak", "2019-05-12",
                "1985-12-12", "Warszawa", "Leśna",
                "00-003", "888-888")
emp3 = Employee("Piotr", "Zieliński", "2021-10-10",
                "1995-07-07", "Kraków", "Rynek",
                "30-002", "777-777")


stud1 = Student("Marek", "Sigma")
stud2 = Student("Kasia", "Parówka")
stud3 = Student("Tomek", "Poziomek")


b1 = Book(lib1, "2000", "J.K.",
          "Rowling", 300)
b2 = Book(lib1, "1954", "J.R.R.",
          "Tolkien", 500)
b3 = Book(lib2, "1965", "Frank",
          "Herbert", 400)
b4 = Book(lib2, "1986", "Stephen",
          "King", 600)
b5 = Book(lib1, "1925", "F.",
          "Fitzgerald", 200)


order1 = Order(emp1, stud1, [b1, b2], "2023-11-24")


order2 = Order(emp3, stud2, [b3], "2023-11-25")


print(order1)
print()
print(order2)
