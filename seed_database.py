import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
# This is a module from Python’s standard library. It contains code related to working with your computer’s operating system.

os.system('dropdb ratings')
os.system('createdb ratings')

# Remember — we imported model and server instead of importing individual functions.
# If we had written from model import db, we’d be able to access db. 
# However, since it’s just import model, you have to go through model before you can access db.
model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can user them to create fake ratings later
movies_in_db = []

# Loop over the movie_data list of dictionary and create Movie object
# Then add it to the dictionary of movie
for movie in movie_data:
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    
    date_str = movie['release_date']
    format = '%Y-%m-%d'
    date = datetime.strptime(date_str, format)
    release_date = date

    db_movie = crud.create_movie(title, 
                                 overview,
                                 release_date,
                                 poster_path)
    
    movies_in_db.append(db_movie)


# Create user

for n in range(10):
    email = f'user{n}@gmail.com'
    password = 'anything'

    user = crud.create_user(email, password)

    for k in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1,5)
        crud.create_rating(user, random_movie, score)
         