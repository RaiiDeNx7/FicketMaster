from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key_here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ficketmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MODELS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    bio = db.Column(db.String(500), default="")
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    date = db.Column(db.String(20))
    location = db.Column(db.String(120))
    tickets_available = db.Column(db.Integer)
    price = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Event {self.name}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='tickets')
    event = db.relationship('Event', backref='tickets')


# ROUTES

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
        price = request.form.get('price', type=float) or 0.0

        new_event = Event(name=name, date=date, location=location, tickets_available=tickets, price=price)
        db.session.add(new_event)
        db.session.commit()
        flash('New event created!')
        return redirect(url_for('events_page'))

    all_events = Event.query.all()
    return render_template('events.html', events=all_events)

@app.route('/booking/<int:event_id>')
def booking_page(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('booking.html', event=event)

@app.route('/api/book', methods=['POST'])
def book_tickets():
    try:
        user_id = int(request.form.get('user_id'))
        event_id = int(request.form.get('event_id'))
        tickets_requested = int(request.form.get('tickets'))
    except (TypeError, ValueError):
        flash("Invalid input. Please try again.")
        return redirect(url_for('events_page'))

    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if not user or not event:
        flash("User or Event not found.")
        return redirect(url_for('events_page'))

    if tickets_requested <= 0:
        flash("Please select at least one ticket.")
        return redirect(url_for('booking_page', event_id=event.id))

    if event.tickets_available < tickets_requested:
        flash("Not enough tickets available.")
        return redirect(url_for('booking_page', event_id=event.id))

    event.tickets_available -= tickets_requested
    ticket = Ticket(user_id=user.id, event_id=event.id, quantity=tickets_requested)
    db.session.add(ticket)
    db.session.commit()

    flash(f"Successfully booked {tickets_requested} ticket(s) for {event.name}!")
    return redirect(url_for('profile_page'))

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
            flash("Email already registered.")
            return redirect(url_for('signup'))  # Not 'index'


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
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    tickets = Ticket.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, tickets=tickets)

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "dob": user.dob.isoformat(),
            "bio": user.bio
        })
    return jsonify({"message": "User not found"}), 404

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        "id": e.id,
        "name": e.name,
        "date": e.date,
        "location": e.location,
        "tickets_available": e.tickets_available,
        "price": e.price
    } for e in events])

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    event = Event.query.get_or_404(event_id)
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
    if not os.path.exists('ficketmaster.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

