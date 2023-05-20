from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from os import path
from flask_login import LoginManager, current_user
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
import requests
from wtforms import StringField, DateTimeField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired
from datetime import datetime
from requests import request


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Venue, Ticket, Show ,Movie, Tag

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # admin_login_manager = LoginManager()
    # admin_login_manager.init_app(app)
    # admin_login_manager.login_view = 'admin.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin = Admin(app, base_template='baseadmin.html', template_mode='bootstrap4')
    # admin = Admin(app)

    class BaseForm(FlaskForm):
        class Meta:
            csrf = False
        
    class BaseView(ModelView):
        form_base_class = BaseForm
        def is_accessible(self):
            if not current_user.is_authenticated:
                return False
            if current_user.role != 'admin':
                print('not admin')
                return False
            return True
    
        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('auth.login'))

    class MovieForm(BaseForm):
        name = StringField('Name', validators=[DataRequired()])
        rating = StringField('Rating', validators=[DataRequired()])
        poster = StringField('Poster')
        desc = StringField('Description')
        tags = QuerySelectMultipleField('Tags', query_factory=lambda: Tag.query.all(), get_label='name')

    class MovieView(BaseView):
        form = MovieForm
        
    class ShowForm(BaseForm):
        movie = QuerySelectField('Movie', query_factory=lambda: Movie.query.all(), get_label='name')
        venue = QuerySelectField('Venue', query_factory=lambda: Venue.query.all(), get_label='name')
        time = DateTimeField('Time',validators=[DataRequired()], format='%d-%m-%y %H:%M:00', default=datetime.now().replace(year=datetime.now().year)
    )

    class ShowView(BaseView):
        form = ShowForm
        column_display_pk = True
        column_hide_backrefs = False
        column_list = ('id', 'venue.name', 'movie.name', 'time')

    class TicketForm(FlaskForm):
        venue = QuerySelectField('Venue', query_factory=lambda: Venue.query.all(), get_label='id')
        show = QuerySelectField('Show', query_factory=lambda: Show.query.all(), get_label='id')
        user = QuerySelectField('User', query_factory=lambda: User.query.all(), get_label='id')
        
    
    class TicketView(BaseView):
        with app.app_context():
            shows = Show.query.all()
            venues = Venue.query.all()
        form = TicketForm
        column_display_pk = True
        column_hide_backrefs = False
        column_list = ('id', 'venue.name', 'show.name', 'user.username')

    admin.add_view(BaseView(User, db.session))
    admin.add_view(BaseView(Venue, db.session))
    admin.add_view(TicketView(Ticket, db.session))
    admin.add_view(MovieView(Movie, db.session))
    admin.add_view(ShowView(Show, db.session))
    admin.add_view(BaseView(Tag, db.session))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

