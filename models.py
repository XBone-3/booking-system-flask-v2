from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from statics import MONTHS
from passlib.hash import sha256_crypt

class Conf:
    def __init__(self, app, password) -> None:
        self.app = app
        self.password = password
        self.config_app()

    def config_app(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://call_me_x:{self.password}@localhost/test_db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'


    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    mobile = db.Column(db.String(45), unique=True)
    email = db.Column(db.String(100), unique=True)
    online = db.Column(db.Boolean, default = 0)
    admin = db.Column(db.Boolean, default = 0)
    registered_ts = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, name, username, password, mobile, email):
        self.name = name
        self.username = username
        self.password = password
        self.mobile = mobile
        self.email = email
        self.online = 0
        self.admin = 0
        self.registered_ts = datetime.utcnow()

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)
    
    def is_admin(self):
        if self.admin == 1:
            return True
        return False
    

class Slots(db.Model):
    __tablename__ = 'slots'


    slot_id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String(45), nullable=False)
    courtname = db.Column(db.String(45), nullable=False)
    timeslot = db.Column(db.String(45), nullable=False)
    availability = db.Column(db.Boolean, default=True)
    date = db.Column(db.DateTime, default=datetime.now().date())

    def __init__(self, sport, courtname, timeslot, availability=1, date=datetime.now().date()):
        self.sport = sport
        self.courtname = courtname
        self.timeslot = timeslot
        self.availability = availability
        self.date = date

class Bookings(db.Model):
    __tablename__ = "bookings"


    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    sport = db.Column(db.String(45), nullable=False)
    courtname = db.Column(db.String(45), nullable=False)
    year = db.Column(db.Integer)
    month = db.Column(db.String(12))
    day = db.Column(db.Integer)
    timeslot = db.Column(db.String(45), nullable=False)
    comment = db.Column(db.String(255), default="You did not comment on this booking.. But, we think you enjoyed a lot.")

    def __init__(self, user_id, sport, courtname, year, month, day, timeslot, comment):
        self.user_id = user_id
        self.sport = sport
        self.courtname = courtname
        self.year = year
        self.month = month
        self.day = day
        self.timeslot = timeslot
        self.comment = comment


