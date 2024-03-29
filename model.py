"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A User"""

    __tablename__= 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects


    def __repr__(self):
        """Show User info"""
        return(f'<user_id = {self.user_id}, email = {self.email}>')


class Movie(db.Model):
    """A Movie"""

    __tablename__= 'movies'

    movie_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    password = db.Column(db.String)
    poster_path = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        """Show Movie info"""
        return(f'<movie_id = {self.movie_id}, title = {self.title}>')


class Rating(db.Model):
    """A rating"""

    __tablename__= 'ratings'

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # Suppose we have rating = Rating.query.get(1) - Get a rating by primary key
    # Create 2 attributes so that rating.movie can return the Movie object related to the rating
    # And rating.user can return the User object related to the rating
    movie = db.relationship('Movie', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        """Show Rating info"""
        return(f'<rating_id = {self.rating_id}, score = {self.score}>')


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    # Configuration: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
