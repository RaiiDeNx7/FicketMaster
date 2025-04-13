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


    # Create sample events
    event1 = Event(
        name="Jazz Night 2025",
        date=date(2025, 7, 10),  # Ensure date is a date object
        location="City Arena",
        tickets_available=50
    )

    event2 = Event(
        name="Rock Fest",
        date=date(2025, 8, 15),  # Ensure date is a date object
        location="Downtown Park",
        tickets_available=150
    )

    event3 = Event(
        name="Tech Expo",
        date=date(2025, 9, 5),  # Ensure date is a date object
        location="Convention Center",
        tickets_available=300
    )

    event4 = Event(
    name="Classical Concert",
    date="2025-07-25",
    location="Opera House",
    tickets_available=100
    )

    event5 = Event(
    name="Food Festival",
    date="2025-08-01",
    location="Central Park",
    tickets_available=200
    )

    event6 = Event(
    name="Comedy Night",
    date="2025-09-12",
    location="Comedy Club",
    tickets_available=75
    )

    event7 = Event(
    name="Indie Music Fest",
    date="2025-09-20",
    location="Greenfield Stadium",
    tickets_available=120
    )

    event8 = Event(
    name="Film Screening: Sci-Fi Classics",
    date="2025-10-05",
    location="Downtown Theater",
    tickets_available=250
    )

    event9 = Event(
    name="Fashion Show 2025",
    date="2025-10-15",
    location="Grand Hall",
    tickets_available=150
    )

    event10 = Event(
    name="Live DJ Set",
    date="2025-11-01",
    location="Nightclub X",
    tickets_available=300
    )

    # Add to session and commit
    db.session.add(user)
    db.session.add_all([event1,event2,event3,event4, event5, event6, event7, event8, event9, event10])
    db.session.commit()

    print("✅ Database seeded with sample data.")
