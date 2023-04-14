from flask import Blueprint, render_template, request, flash, jsonify, abort
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from functools import wraps
from datetime import datetime

views = Blueprint('views', __name__)

# def admin_login_required(func):
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if not current_user.is_authenticated or not current_user.is_admin:
#             abort(403)  # return a 403 Forbidden error if the user is not an admin
#         return func(*args, **kwargs)
#     return login_required(decorated_view)



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

@views.route('/bookings', methods=['GET'])
@login_required
def bookings():
    tickets = Ticket.query.filter_by(user_id=current_user.id)
    shows = Show.query.all()
    venues = Venue.query.all()
    print(venues)
    return render_template("bookings.html", user=current_user, tickets=tickets, shows=shows, venues=venues)

# @views.route('/ticketnew', methods=['GET','POST'])
# @login_required
# def ticket_new():
#     if request.method == "POST":
#         print(request.form)

#     ticket = Ticket.query.all()
#     return render_template("ticket.html", user=current_user, ticket=ticket)

# @views.route('/ticketnew/add', methods=['GET','POST'])
# @login_required
# def ticket_new_add():
#     if request.method == "POST":
#         data=request.form
#         tk=Ticket(user_id=data.get('user'), show_id=data.get('show'), venue_id=data.get('venue'))
#         db.session.add(tk)
#         db.session.commit()
#     return render_template("ticketadd.html", user=current_user)

# @views.route('/book/<int:show_id>', methods=['GET','POST'])
# @login_required
# def book_ticket():


# @views.route('/admin' , methods=['GET', 'POST'])
# @admin_login_required
# def admin():
#     return render_template("admin.html", user=current_user)


# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
