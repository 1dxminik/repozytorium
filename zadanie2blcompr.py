def pomnoz_elementy(lista_liczb):
    return [x * 2 for x in lista_liczb]


moje_liczby = [1, 5, 10, 3, 8]


wynik = pomnoz_elementy(moje_liczby)


print(f"Lista wejściowa: {moje_liczby}")
print(f"Lista zwrócona:  {wynik}")

