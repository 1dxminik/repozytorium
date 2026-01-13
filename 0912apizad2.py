from fastapi import FastAPI
import csv

app = FastAPI()



class Movie:
    def __init__(self, movie_id, title, genres):
        self.id = movie_id
        self.title = title
        self.genres = genres


@app.get('/')
async def get_index():
    return {"message": "Hello World"}


@app.get('/movies')
async def get_movies():
    movies_list = []

    with open('movies.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)


        for row in csv_reader:

            if len(row) >= 3:

                movie_obj = Movie(movie_id=row[0], title=row[1], genres=row[2])

                movies_list.append(movie_obj.__dict__)


    return movies_list