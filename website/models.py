from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# show_venue = db.Table(
#     'show_venue',
#     db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True),
#     db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
# )

movie_tag = db.Table('movie_tag',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


# class Note(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # data = db.Column(db.String(10000))
    # date = db.Column(db.DateTime(timezone=True), default=func.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    capacity = db.Column(db.Integer)
    show = db.relationship('Show', backref='venue')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    rating = db.Column(db.Float)
    tags = db.relationship('Tag', secondary=movie_tag, backref=db.backref('movie', lazy='dynamic'))
    show = db.relationship('Show', backref='movie')
    description = db.Column(db.String(10000), default = "No description available")
    poster = db.Column(db.String(10000), default="/static/img/poster.jpg")

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # venue = db.relationship('Venue', backref=db.backref('tickets_venue', lazy='dynamic'))
    # show = db.relationship('Show', backref=db.backref('tickets_show', lazy='dynamic'))
    # user = db.relationship('User', backref=db.backref('tickets_user'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    venue_id = db.Column(db.String, db.ForeignKey('venue.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    tickets = db.relationship('Ticket', backref='user')
    role = db.Column(db.String(20), default='user')
    # notes = db.relationship('Note')


# class Dummy(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150))
#     venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))


    # venue = db.relationship('Venue', backref=db.backref('tickets_venue', lazy='dynamic'))
    # show = db.relationship('Show', backref=db.backref('tickets_show', lazy='dynamic'))
    # user = db.relationship('User', backref=db.backref('tickets_user', lazy='dynamic'))

    # def __repr__(self):
    #     return f"Ticket {self.id} - {self.show.name} at {self.venue.name} for {self.user.email}"