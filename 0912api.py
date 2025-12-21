import csv
from fastapi import FastAPI


app = FastAPI()


# --- MODELE DANYCH (KLASY) ---

# 1. Model dla filmów (dostosowany do Twojego zrzutu ekranu)
class Movie:
    def __init__(self, movieId, title, genres):
        self.id = movieId
        self.title = title
        self.genres = genres

# 2. Model dla linków (links.csv: movieId, imdbId, tmdbId)
class Link:
    def __init__(self, movieId, imdbId, tmdbId):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId


# 3. Model dla ocen (ratings.csv: userId, movieId, rating, timestamp)
class Rating:
    def __init__(self, userId, movieId, rating, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp


# 4. Model dla tagów (tags.csv: userId, movieId, tag, timestamp)
class Tag:
    def __init__(self, userId, movieId, tag, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = timestamp


# --- ENDPOINTY ---

@app.get("/movies")
def get_movies():
    results = []
    # Otwieramy plik movies.csv
    with open("movies.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pomijamy nagłówek

        for row in reader:
            # Tworzymy obiekt (row[0]=movieId, row[1]=title, row[2]=genres)
            movie = Movie(row[0], row[1], row[2])
            results.append(movie.__dict__)

    return results


@app.get("/links")
def get_links():
    results = []
    with open("links.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            # links.csv ma 3 kolumny
            if len(row) >= 3:
                link = Link(row[0], row[1], row[2])
                results.append(link.__dict__)
    return results


@app.get("/ratings")
def get_ratings():
    results = []
    with open("ratings.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        # Ograniczenie dla wydajności (ratings.csv bywa ogromny!)
        # Wczytujemy np. pierwsze 100 ocen, żeby nie zawiesić przeglądarki
        counter = 0
        for row in reader:
            rating = Rating(row[0], row[1], row[2], row[3])
            results.append(rating.__dict__)

            counter += 1
            if counter >= 100:  # Usuń ten if, jeśli chcesz wczytać wszystko
                break

    return results


@app.get("/tags")
def get_tags():
    results = []
    with open("tags.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row) >= 4:
                tag = Tag(row[0], row[1], row[2], row[3])
                results.append(tag.__dict__)
    return results