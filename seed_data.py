from app import db, User, Event, app  # Make sure to import app
from datetime import date

# Recreate all tables (use only if you're OK wiping existing data)
with app.app_context():  # Ensure that we are within the app context
    db.drop_all()
    db.create_all()

    # Create sample user
    user = User(
        name="Jane Doe",
        email="jane.doe@example.com",
        dob=date(1995, 4, 20),
        bio="Hi, I'm Jane! Excited for concerts!",
        password="samplepassword"  # Add a password here
    )

    # Create sample events with price included
    event1 = Event(
        name="Jazz Night 2025",
        date=date(2025, 7, 10),
        location="City Arena",
        tickets_available=50,
        price=25.00  # Added price
    )

    event2 = Event(
        name="Rock Fest",
        date=date(2025, 8, 15),
        location="Downtown Park",
        tickets_available=150,
        price=19.99  # Added price
    )

    event3 = Event(
        name="Tech Expo",
        date=date(2025, 9, 5),
        location="Convention Center",
        tickets_available=300,
        price=10.00  # Added price
    )

    event4 = Event(
        name="Classical Concert",
        date=date(2025, 7, 25),
        location="Opera House",
        tickets_available=100,
        price=40.00  # Added price
    )

    event5 = Event(
        name="Food Festival",
        date=date(2025, 8, 1),
        location="Central Park",
        tickets_available=200,
        price=15.00  # Added price
    )

    event6 = Event(
        name="Comedy Night",
        date=date(2025, 9, 12),
        location="Comedy Club",
        tickets_available=75,
        price=30.00  # Added price
    )

    event7 = Event(
        name="Indie Music Fest",
        date=date(2025, 9, 20),
        location="Greenfield Stadium",
        tickets_available=120,
        price=22.50  # Added price
    )

    event8 = Event(
        name="Film Screening: Sci-Fi Classics",
        date=date(2025, 10, 5),
        location="Downtown Theater",
        tickets_available=250,
        price=18.00  # Added price
    )

    event9 = Event(
        name="Fashion Show 2025",
        date=date(2025, 10, 15),
        location="Grand Hall",
        tickets_available=150,
        price=50.00  # Added price
    )

    event10 = Event(
        name="Live DJ Set",
        date=date(2025, 11, 1),
        location="Nightclub X",
        tickets_available=300,
        price=35.00  # Added price
    )

    # Add to session and commit
    db.session.add(user)
    db.session.add_all([event1, event2, event3, event4, event5, event6, event7, event8, event9, event10])
    db.session.commit()

    print("✅ Database seeded with sample data.")
