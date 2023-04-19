from flask import Blueprint, render_template, request, flash, jsonify, abort
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import json


views = Blueprint('views', __name__)
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')
    movies = Movie.query.all()
    return render_template("home.html", user=current_user, movies=movies)

@views.route('/movies', methods=['GET'])
@login_required
def movies():
    movies = Movie.query.all()
    return render_template("movies.html", user=current_user, movies=movies)

@views.route('/movies/<int:movie_id>', methods=['GET'])
@login_required
def movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    return render_template("movie.html", user=current_user, movie=movie)

@views.route('/movies/<int:movie_id>/book', methods=['GET', 'POST'])
@login_required
def book_movie(movie_id):

    if request.method == "POST":
        data=request.form
        print(data)

        show_id = data.get('show-id')
        ticket_count = data.get('ticket-count')
        show = Show.query.filter_by(id=show_id).first()
        print(show.id, show.venue.id, current_user.id, ticket_count)

        for i in range(int(ticket_count)):
            ticket = Ticket(user_id=current_user.id, show_id=show.id, venue_id=show.venue.id)
            db.session.add(ticket)    
        db.session.commit()
        print(ticket_count)


    movie = Movie.query.filter_by(id=movie_id).first()
    shows = Show.query.filter_by(movie_id=movie_id)
    # print(movie,shows[0])
    return render_template("book-movie.html", user=current_user, shows=shows, movie=movie)

@views.route('/bookings', methods=['GET,POST'])
@login_required
def bookings():
    tickets = Ticket.query.filter_by(user_id=current_user.id)
    shows = Show.query.all()
    venues = Venue.query.all()
    print(venues)
    return render_template("bookings.html", user=current_user, tickets=tickets, shows=shows, venues=venues)

@views.route('/testapi/', methods=['GET','POST'])
def testapi():
    
    if request.method == 'POST':
        formdata = request.form
        movieTitle = formdata['movieTitle']
        url = 'http://www.omdbapi.com/?t={}&plot=full&apikey={}'.format(movieTitle, OMDB_API_KEY)
        response = requests.get(url)
        Data = response.json()
        # Data = json.loads(data)
        return render_template('testapi.html', user=current_user, moviesuccess="True", title=Data['Title'], rating=Data['imdbRating'], poster=Data['Poster'])

    return render_template('testapi.html', user=current_user)

# @views.route('/addmovie/', methods=['GET','POST'])
# def addmovie():
#     if request.method == 'POST':
#         formdata = request.form
#         movieTitle = formdata['movieTitle']
#         url = 'http://www.omdbapi.com/?t={}&plot=full&apikey={}'.format(movieTitle, OMDB_API_KEY)
#         response = requests.get(url)
#         Data = response.json()
#         # Data = json.loads(data)
#         # new_movie = Movie(title=Data['Title'], rating=Data['imdbRating'], poster=Data['Poster'])
#         # db.session.add(new_movie)
#         # db.session.commit()
#         return render_template('addmovie.html', user=current_user, moviesuccess="True", title=Data['Title'], rating=Data['imdbRating'], poster=Data['Poster'])

#     return render_template('addmovie.html', user=current_user)

@views.route('/chart/', methods=['GET'])
def chart():
    return render_template('chart.html', user=current_user)