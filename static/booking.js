// Event listener to ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
  
  // Get the booking form element
  const form = document.getElementById('booking-form');

  // Add an event listener for the form submission
  form.addEventListener('submit', (e) => {
    e.preventDefault();  // Prevent the default form submission behavior

    // Get the number of tickets, user ID, and event ID from the form
    const tickets = document.getElementById('tickets').value;
    const userId = form.querySelector('input[name="user_id"]').value;
    const eventId = form.querySelector('input[name="event_id"]').value;

    // Send a POST request to the backend API to book the tickets
    fetch('/api/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },  // Set the request content type to JSON
      body: JSON.stringify({
        user_id: userId,  // Send the user ID
        event_id: eventId,  // Send the event ID
        tickets: tickets  // Send the number of tickets requested
      })
    })
    .then(res => res.json())  // Parse the response as JSON
    .then(data => {
      alert(data.message);  // Display the response message from the backend
      window.location.href = '/profile'; // Redirect to the profile page after booking
    });
  });
});

  