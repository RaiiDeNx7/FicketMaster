from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.Enum('customer', 'admin'), default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    total_tickets = db.Column(db.Integer)
    available_tickets = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Enum('pending', 'completed', 'failed'))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
