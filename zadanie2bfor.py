numbers = [1, 2, 3, 4, 5]


def liczby(numbers):
    newnumbers = []
    for i in numbers:
        i = i * 2
        newnumbers.append(i)
    return newnumbers


print(liczby(numbers))
