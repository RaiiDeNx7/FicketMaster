from app import app, db, User, Event

with app.app_context():
    # Recreate all tables (CAUTION: This will wipe existing data)
    db.drop_all()
    db.create_all()

    # Create sample user
    user = User(
        name="Jane Doe",
        email="jane.doe@example.com",
        dob="1995-04-20",
        bio="Hi, I'm Jane! Excited for concerts!"
    )

    # Create sample events
    event1 = Event(
        name="Jazz Night 2025",
        date="2025-07-10",
        location="City Arena",
        tickets_available=50
    )

    event2 = Event(
        name="Rock Fest",
        date="2025-08-15",
        location="Downtown Park",
        tickets_available=150
    )

    event3 = Event(
        name="Tech Expo",
        date="2025-09-05",
        location="Convention Center",
        tickets_available=300
    )

    # Add everything to the session and commit
    db.session.add(user)
    db.session.add_all([event1, event2, event3])
    db.session.commit()

    print("✅ Database seeded with sample data.")

