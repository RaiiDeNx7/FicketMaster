from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_folder='static')

# In-memory storage for users, events, and bookings
users = {
    1: {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "dob": "1990-01-01", "bio": "Hello, I'm John!"}
}

events = {
    1: {"id": 1, "name": "Concert A", "date": "2025-05-01", "location": "Stadium A", "tickets_available": 100},
    2: {"id": 2, "name": "Concert B", "date": "2025-06-01", "location": "Stadium B", "tickets_available": 200}
}

bookings = []

# Serve the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Serve the events page (events.html)
@app.route('/events')
def events_page():
    return render_template('events.html', events=events)

# Serve the profile page (profile.html)
@app.route('/profile')
def profile_page():
    # Assuming the user ID is 1 for now
    user = users.get(1)
    return render_template('profile.html', user=user)

# Get all events
@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(list(events.values()))

# Book tickets for an event
@app.route('/api/book', methods=['POST'])
def book_tickets():
    user_id = request.json.get('user_id')
    event_id = request.json.get('event_id')
    tickets = request.json.get('tickets')

    # Check if event exists and has enough tickets
    event = events.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    if event["tickets_available"] < tickets:
        return jsonify({"message": "Not enough tickets available"}), 400

    # Update tickets availability
    event["tickets_available"] -= tickets

    # Create a booking record
    booking = {"user_id": user_id, "event_id": event_id, "tickets": tickets}
    bookings.append(booking)

    return jsonify({"message": "Tickets booked successfully!"}), 201

# Get user profile (API endpoint)
@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

