document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('booking-form');
  
    form.addEventListener('submit', (e) => {
      e.preventDefault();
  
      const tickets = document.getElementById('tickets').value;
      const userId = form.querySelector('input[name="user_id"]').value;
      const eventId = form.querySelector('input[name="event_id"]').value;
  
      fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          event_id: eventId,
          tickets: tickets
        })
      })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        window.location.href = '/profile'; // Redirect to profile page after booking
      });
    });
  });
  
  