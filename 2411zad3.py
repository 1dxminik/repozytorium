class Property:
    def __init__(self, area, rooms: int, price, adress):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.adress = adress

    def __str__(self):
        return f'{self.area} {self.rooms} {self.price} {self.adress}'


class House(Property):
    def __init__(self, area, rooms, price, adress, plot: int):
        super().__init__(area, rooms, price, adress)

        self.plot = plot

    def __str__(self):
        return (f'{self.area} {self.rooms} {self.price} {self.adress} '
                f'{self.plot}')


class Flat(Property):
    def __init__(self, area, rooms, price, adress, floor):
        super().__init__(area, rooms, price, adress)

        self.floor = floor

    def __str__(self):
        return (f'{self.area} {self.rooms} {self.price} {self.adress} '
                f'{self.floor}')


dom = House(120, 5, 500000, "Wysoka", 10000)
mieszkanie = Flat(46, 2, 300000, "Wysoka", 10)
print(dom)
print(mieszkanie)
