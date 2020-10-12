"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
# Now let’s configure the Flask instance. 
# It’ll need a secret key (otherwise, flash and session won’t work); we’ll also configure Jinja2 here as well:
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage"""
    return render_template('homepage.html')


@app.route('/movies')
def movie():
    movies = crud.get_movies() # call get movie list function from Crud.py

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>') 
# 'movie_id' is just a variable name. It can be anything like xyz
# What ensures the URL be populated with the right ID is the href tag in all_movies.html
# <a href='/movies/{{ movie.movie_id }}'>{{ movie.title }}</a>
# Then the <movie_id> is passed to the movie_detail function below 
# so that it can retrieve the right movie to display
def movie_detail(movie_id):
    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie = movie)


@app.route('/users', methods=["POST"])
def register_user():
    """ Register a user """
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash ('Cannot create an account wit that email. Try again.')
    else:
        crud.create_user(email,password)
        flash ('Account created! Please login')

    return redirect('/')
    

if __name__ == '__main__':
    # connect to your database before app.run gets called. If you don’t do this, 
    # Flask won’t be able to access your database!
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
