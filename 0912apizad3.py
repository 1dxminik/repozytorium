from fastapi import FastAPI
import csv

app = FastAPI()


class Movie:
    def __init__(self, movie_id, title, genres):
        self.id = movie_id
        self.title = title
        self.genres = genres

class Link:
    def __init__(self, movie_id, imdb_id, tmdb_id):
        self.movieId = movie_id
        self.imdbId = imdb_id
        self.tmdbId = tmdb_id

# 3. Nowy model dla ocen (Ratings)
class Rating:
    def __init__(self, user_id, movie_id, rating, timestamp):
        self.userId = user_id
        self.movieId = movie_id
        self.rating = rating
        self.timestamp = timestamp

# 4. Nowy model dla tagów (Tags)
class Tag:
    def __init__(self, user_id, movie_id, tag, timestamp):
        self.userId = user_id
        self.movieId = movie_id
        self.tag = tag
        self.timestamp = timestamp


@app.get('/')
async def get_index():
    return {"message": "Witaj w API filmowym!"}


@app.get('/movies')
async def get_movies():
    results = []
    try:
        with open('movies.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    # Tworzenie obiektu i serializacja __dict__
                    obj = Movie(row[0], row[1], row[2])
                    results.append(obj.__dict__)
    except FileNotFoundError:
        return {"error": "Plik movies.csv nie istnieje"}
    return results

# Endpoint dla Links
@app.get('/links')
async def get_links():
    results = []
    try:
        with open('links.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    obj = Link(row[0], row[1], row[2])
                    results.append(obj.__dict__)
    except FileNotFoundError:
        return {"error": "Plik links.csv nie istnieje"}
    return results

# Endpoint dla Ratings
@app.get('/ratings')
async def get_ratings():
    results = []
    try:
        with open('ratings.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 4:
                    obj = Rating(row[0], row[1], row[2], row[3])
                    results.append(obj.__dict__)
    except FileNotFoundError:
        return {"error": "Plik ratings.csv nie istnieje"}
    return results

# Endpoint dla Tags
@app.get('/tags')
async def get_tags():
    results = []
    try:
        with open('tags.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # next(reader, None)
            for row in reader:
                if len(row) >= 4:
                    obj = Tag(row[0], row[1], row[2], row[3])
                    results.append(obj.__dict__)
    except FileNotFoundError:
        return {"error": "Plik tags.csv nie istnieje"}
    return results