from backend import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bookings = db.relationship('Booking', backref='user')
    # , lazy=True
    last_login = db.Column(db.DateTime)

class Theatre(db.Model):
    __tablename__ = 'theatres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='theatre', cascade='all, delete-orphan')    # , lazy=True


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(200))
    ticket_price = db.Column(db.Integer, nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatres.id'), nullable=False)
    start_time_hours = db.Column(db.Integer, nullable=False)  # Hours (0-23) for start time
    start_time_minutes = db.Column(db.Integer, nullable=False)  # Minutes (0-59) for start time
    end_time_hours = db.Column(db.Integer, nullable=False)  # Hours (0-23) for end time
    end_time_minutes = db.Column(db.Integer, nullable=False)  # Minutes (0-59) for end time
    bookings = db.relationship('Booking', backref='show', cascade='all, delete-orphan')

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    # total_price = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    