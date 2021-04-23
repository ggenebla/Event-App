from database import db
import datetime


class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    event_title = db.Column("event_title", db.String(200))
    event_description = db.Column("event_description", db.String(100))
    date = db.Column("date", db.String(50))
    # creates a foreign key; referencing the id variable in the User class
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __init__(self, event_title, event_description, date, event_id):
        self.event_title = event_title
        self.event_description = event_description
        self.date = date
        self.event_id = event_id


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()
