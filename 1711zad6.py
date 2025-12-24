def funkcja(a, b):
    c = list(set(a + b))
    d = []
    for x in c:
        x = int(x)
        x = pow(x, 3)
        d.append(x)

    return d


lol = input("Podaj elementy pierwszej listy (tylko cyfry): ").split()
xd = input("Podaj elementy drugiej listy(tylko cyfry): ").split()
print(funkcja(lol, xd))
