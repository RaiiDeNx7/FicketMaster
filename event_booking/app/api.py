from flask import Blueprint, jsonify, request
from .models import Event, Ticket, Payment, db

api = Blueprint('api', __name__)

@api.route('/events')
def get_events():
    events = Event.query.all()
    return jsonify([{
        "id": e.id,
        "name": e.name,
        "description": e.description,
        "location": e.location,
        "price": float(e.price),
        "available_tickets": e.available_tickets
    } for e in events])

@api.route('/book/<int:event_id>', methods=['POST'])
def book_ticket(event_id):
    event = Event.query.get(event_id)
    if event and event.available_tickets > 0:
        # Booking simulation
        ticket = Ticket(user_id=1, event_id=event.id)  # Assume user_id = 1
        payment = Payment(user_id=1, ticket_id=ticket.id, amount=event.price, status='completed')

        event.available_tickets -= 1

        db.session.add(ticket)
        db.session.add(payment)
        db.session.commit()
        return jsonify({"message": "Ticket booked successfully!"})
    return jsonify({"message": "Event not found or sold out"}), 400
