# import your Flask app and database instance
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.models import *

db = SQLAlchemy()
DB_NAME = "database.db"
# app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


# start the Flask shell
with app.app_context():
    # create some dummy users
    tags = [Tag(name='Action'),
    Tag(name='Comedy'),
    Tag(name='Drama'),
    Tag(name='Horror'),
    Tag(name='Romance')
    ]

    venues = [
        Venue(name="PVR", address="VR Mall", city="Vizag", capacity=100),
        Venue(name="INOX", address="Daba Gardens", city="Vizag", capacity=100),
        Venue(name="Cinepolis", address="Daba Gardens", city="Vizag", capacity=100),
        Venue(name="PVR", address="Daba Gardens", city="Vizag", capacity=100),
        Venue(name="INOX", address="VR Mall", city="Vizag", capacity=100),
    ]

    movies = [
        Movie(name="Avengers", rating=4.5),
        Movie(name="Avengers: Endgame", rating=4.5),
        Movie(name="Avengers: Infinity War", rating=4.5),
        Movie(name="Avengers: Age of Ultron", rating=4.5),
        Movie(name="Captain America: The First Avenger", rating=4.5),
    ]

    shows = [
        Show(movie_id=1, venue_id=1),
        Show(movie_id=1, venue_id=2),
        Show(movie_id=1, venue_id=3),
        Show(movie_id=1, venue_id=4),
        Show(movie_id=1, venue_id=5)
    ]



    for i in venues, movies, shows, tags:
        for j in i:
            db.session.add(j)

    db.session.commit()

    # print the users to verify they were added
    print(User.query.all())
