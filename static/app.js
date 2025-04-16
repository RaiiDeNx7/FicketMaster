document.addEventListener('DOMContentLoaded', () => {
  // Fetch and display events
  fetch('/api/events')
    .then(response => response.json())
    .then(events => {
      const eventList = document.getElementById('event-list');
      events.forEach(event => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${event.name} - $${event.price.toFixed(2)}
          <button onclick="window.location.href='/booking/${event.id}'">Book Now</button>
        `;
        eventList.appendChild(li);
      });
    });

  // Handle ticket booking (this part can be removed if you are using booking.html form)
  const bookingForm = document.getElementById('booking-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const tickets = document.getElementById('tickets').value;
      const userId = 1; // Example user id
      const eventId = 1; // Example event id

      fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, event_id: eventId, tickets: tickets })
      })
      .then(response => response.json())
      .then(data => alert(data.message));
    });
  }

  // Fetch user profile data (you can keep this part as is)
  const userId = 1; // Example user id
  fetch(`/api/profile/${userId}`)
    .then(response => response.json())
    .then(user => {
      document.getElementById('user-name').textContent = user.name;
      document.getElementById('user-email').textContent = user.email;
      document.getElementById('user-dob').textContent = user.dob;
      document.getElementById('user-bio').textContent = user.bio;
    });
});
