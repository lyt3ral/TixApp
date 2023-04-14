import factory
from .models import User, Venue, Show, Movie, Tag, Ticket
from .. import db

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')


class VenueFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Venue
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Sequence(lambda n: 'Venue {}'.format(n))
    address = factory.Faker('address')
    city = factory.Faker('city')
    capacity = factory.Sequence(lambda n: 100 + n)


class ShowFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Show
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    time = factory.Faker('date_time')
    movie = factory.SubFactory('MovieFactory')
    venue = factory.SubFactory('VenueFactory')


class MovieFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Movie
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Sequence(lambda n: 'Movie {}'.format(n))
    rating = factory.Sequence(lambda n: 3.5 + n / 10)


class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tag
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')


class TicketFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Ticket
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    user = factory.SubFactory('UserFactory')
    show = factory.SubFactory('ShowFactory')
    venue = factory.SubFactory('VenueFactory')
