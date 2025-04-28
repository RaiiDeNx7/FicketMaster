from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
import os

# Initialize the Flask application
app = Flask(__name__, static_folder='static')

# Set the secret key for session management
app.secret_key = 'your_secret_key_here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ficketmaster.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)  # Initialize the database object
migrate = Migrate(app, db)  # Initialize migration object

# MODELS

# User model: Represents the users of the system
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # User ID (Primary Key)
    name = db.Column(db.String(100), nullable=False)  # User's full name
    email = db.Column(db.String(100), unique=True, nullable=False)  # User's email (Unique)
    dob = db.Column(db.Date, nullable=False)  # User's date of birth
    bio = db.Column(db.String(500), default="")  # User's bio (Optional)
    password = db.Column(db.String(100), nullable=False)  # Hashed password for user authentication

    def __repr__(self):
        return f'<User {self.name}>'  # String representation of the User object

# Event model: Represents the events that users can book tickets for
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Event ID (Primary Key)
    name = db.Column(db.String(120))  # Event name
    date = db.Column(db.String(20))  # Event date
    location = db.Column(db.String(120))  # Event location
    tickets_available = db.Column(db.Integer)  # Number of tickets available
    price = db.Column(db.Float, default=0.0)  # Price per ticket

    def __repr__(self):
        return f'<Event {self.name}>'  # String representation of the Event object

# Ticket model: Represents a ticket booked by a user for an event
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Ticket ID (Primary Key)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign Key to the User model
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)  # Foreign Key to the Event model
    quantity = db.Column(db.Integer, nullable=False)  # Number of tickets booked

    user = db.relationship('User', backref='tickets')  # Relationship to User model
    event = db.relationship('Event', backref='tickets')  # Relationship to Event model


# ROUTES

# Home page
@app.route('/')
def index():
    return render_template('index.html')  # Renders the index page

# Events page: Displays all events and allows creation of new events
@app.route('/events', methods=['GET', 'POST'])
def events_page():
    if request.method == 'POST':  # If the form is submitted
        name = request.form['name']
        date = request.form['date']
        location = request.form['location']
        tickets = int(request.form['tickets'])  # Convert tickets to integer
        price = request.form.get('price', type=float) or 0.0  # Set price to 0.0 if not provided

        # Create a new event instance
        new_event = Event(name=name, date=date, location=location, tickets_available=tickets, price=price)
        db.session.add(new_event)  # Add event to the session
        db.session.commit()  # Commit the transaction
        flash('New event created!')  # Flash message
        return redirect(url_for('events_page'))  # Redirect to events page

    # Retrieve all events from the database
    all_events = Event.query.all()
    return render_template('events.html', events=all_events)  # Render the events page with the events list

# Booking page: Allows users to book tickets for a specific event
@app.route('/booking/<int:event_id>')
def booking_page(event_id):
    event = Event.query.get_or_404(event_id)  # Retrieve event by ID or return 404 if not found
    return render_template('booking.html', event=event)  # Render the booking page with event details

# API route for booking tickets
@app.route('/api/book', methods=['POST'])
def book_tickets():
    try:
        user_id = int(request.form.get('user_id'))  # Get user ID from form
        event_id = int(request.form.get('event_id'))  # Get event ID from form
        tickets_requested = int(request.form.get('tickets'))  # Get number of tickets requested
    except (TypeError, ValueError):
        flash("Invalid input. Please try again.")  # Flash error message for invalid input
        return redirect(url_for('events_page'))  # Redirect to events page

    user = User.query.get(user_id)  # Retrieve the user by ID
    event = Event.query.get(event_id)  # Retrieve the event by ID

    if not user or not event:  # If user or event is not found
        flash("User or Event not found.")  # Flash error message
        return redirect(url_for('events_page'))  # Redirect to events page

    if tickets_requested <= 0:  # If no tickets are selected
        flash("Please select at least one ticket.")  # Flash error message
        return redirect(url_for('booking_page', event_id=event.id))  # Redirect to booking page

    if event.tickets_available < tickets_requested:  # If not enough tickets are available
        flash("Not enough tickets available.")  # Flash error message
        return redirect(url_for('booking_page', event_id=event.id))  # Redirect to booking page

    # Decrease the number of available tickets and create a ticket record
    event.tickets_available -= tickets_requested
    ticket = Ticket(user_id=user.id, event_id=event.id, quantity=tickets_requested)
    db.session.add(ticket)  # Add ticket to session
    db.session.commit()  # Commit the transaction

    flash(f"Successfully booked {tickets_requested} ticket(s) for {event.name}!")  # Flash success message
    return redirect(url_for('profile_page'))  # Redirect to user profile page

# User signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # If the form is submitted
        name = request.form['name']
        email = request.form['email']
        dob_str = request.form['dob']
        password = request.form['password']
        bio = request.form.get('bio', '')  # Default bio if not provided

        # Validate the date of birth format and ensure it's in the past
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()  # Convert string to date
            if dob >= datetime.today().date():  # If DOB is not in the past
                flash("Date of birth must be in the past.")
                return redirect(url_for('signup'))
        except ValueError:
            flash("Invalid date format for date of birth.")  # Flash error if DOB format is invalid
            return redirect(url_for('signup'))

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash("Email already registered.")  # Flash error message if email exists
            return redirect(url_for('signup'))

        # Hash the password before storing it
        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, dob=dob, password=hashed_pw, bio=bio)
        db.session.add(new_user)  # Add new user to session
        db.session.commit()  # Commit the transaction
        flash('Account created! You can now log in.')  # Flash success message
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('signup.html')  # Render signup page

# User login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If the form is submitted
        email = request.form['email']
        password = request.form['password']

        # Retrieve user by email
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):  # Check if password matches
            session['user_id'] = user.id  # Store user ID in session
            flash('Logged in successfully!')  # Flash success message
            return redirect(url_for('index'))  # Redirect to homepage
        flash('Invalid email or password.')  # Flash error message if login fails
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('login.html')  # Render login page

# Logout route: Clears the session and logs the user out
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.')  # Flash logout message
    return redirect(url_for('index'))  # Redirect to homepage

# User profile page: Displays user's profile and booked tickets
@app.route('/profile')
def profile_page():
    if 'user_id' not in session:  # If user is not logged in
        flash("Please log in to view your profile.")  # Flash message
        return redirect(url_for('login'))  # Redirect to login page

    user = User.query.get(session['user_id'])  # Retrieve user by session ID
    tickets = Ticket.query.filter_by(user_id=user.id).all()  # Retrieve all tickets booked by user
    return render_template('profile.html', user=user, tickets=tickets)  # Render profile page

# API route to get user profile in JSON format
@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)  # Retrieve user by ID
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "dob": user.dob.isoformat(),  # Convert DOB to ISO format
            "bio": user.bio
        })
    return jsonify({"message": "User not found"}), 404  # Return 404 if user not found

# API route to get all events in JSON format
@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()  # Retrieve all events from the database
    return jsonify([{
        "id": e.id,
        "name": e.name,
        "date": e.date,
        "location": e.location,
        "tickets_available": e.tickets_available,
        "price": e.price
    } for e in events])

# API route to get specific event details in JSON format
@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    event = Event.query.get_or_404(event_id)  # Retrieve event by ID or return 404 if not found
    return jsonify({
        'id': event.id,
        'name': event.name,
        'date': event.date,
        'location': event.location,
        'price': event.price,
        'tickets_available': event.tickets_available
    })

# Run the app
if __name__ == '__main__':
    # Create the database if it doesn't exist
    if not os.path.exists('ficketmaster.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)  # Start the Flask application in debug mode

