from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from flask_migrate import Migrate



app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key_here'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ficketmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    bio = db.Column(db.String(500), default="")
    password = db.Column(db.String(100), nullable=False)  # Add password field

    def __repr__(self):
        return f'<User {self.name}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    date = db.Column(db.String(20))
    location = db.Column(db.String(120))
    tickets_available = db.Column(db.Integer)
    price = db.Column(db.Float, default=0.0)  # Make sure price is included

    def __repr__(self):
        return f'<Event {self.name}>'



class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    tickets = db.Column(db.Integer)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET', 'POST'])
def events_page():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        location = request.form['location']
        tickets = int(request.form['tickets'])
        # Make sure to get the price as a float from the form
        price = request.form.get('price', type=float)  # This will get the price and convert it to a float

        # If no price is provided, you can set a default value here
        if price is None:
            price = 0.0  # You can set a default value for price if it's not provided

        # Now create a new event with the price included
        new_event = Event(name=name, date=date, location=location, tickets_available=tickets, price=price)
        db.session.add(new_event)
        db.session.commit()
        flash('New event created!')

        return redirect(url_for('events_page'))

    # This part retrieves all events for display
    all_events = Event.query.all()
    return render_template('events.html', events=all_events)


@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        password = request.form['password']
        bio = request.form.get('bio', '')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('signup'))

        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, dob=dob, password=hashed_pw, bio=bio)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        flash('Invalid email or password.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        "id": e.id,
        "name": e.name,
        "date": e.date,
        "location": e.location,
        "tickets_available": e.tickets_available,
        "price": e.price  # Ensure the price field is being returned
    } for e in events])


@app.route('/api/book', methods=['POST'])
def book_tickets():
    data = request.get_json()
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    tickets = data.get('tickets')

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    if event.tickets_available < tickets:
        return jsonify({"message": "Not enough tickets available"}), 400

    event.tickets_available -= tickets
    booking = Booking(user_id=user_id, event_id=event_id, tickets=tickets)
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Tickets booked successfully!"}), 201

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "dob": user.dob,
            "bio": user.bio
        })
    return jsonify({"message": "User not found"}), 404

# Run the app
if __name__ == '__main__':
    if not os.path.exists('ficketmaster.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
