from database import db
import datetime


class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    location = db.Column("location", db.String(200))
    description = db.Column("description", db.String(100))
    date = db.Column("date", db.String(50))
    time = db.Column("time", db.String(50))
    rsvp = db.Column("rsvp", db.String(10))
    rating = db.Column("rate", db.String(10))
    # creates a foreign key; referencing the id variable in the User class
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, location, description, date, time, rsvp, rating, user_id):
        self.title = title
        self.location = location
        self.description = description
        self.date = date
        self.time = time
        self.rsvp = rsvp
        self.rating = rating
        self.user_id = user_id


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    events = db.relationship("Event", backref="User", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

