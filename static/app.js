// Event listener to ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
  
  // Fetch the list of events from the backend API
  fetch('/api/events')
    .then(response => response.json())  // Parse the response as JSON
    .then(events => {
      const eventList = document.getElementById('event-list');  // Get the list element where events will be displayed
      events.forEach(event => {
        // Create a new list item for each event and display its name, price, and a "Book Now" button
        const li = document.createElement('li');
        li.innerHTML = `
          ${event.name} - $${event.price.toFixed(2)}  // Display event name and formatted price
          <button onclick="window.location.href='/booking/${event.id}'">Book Now</button>  // Button to navigate to the booking page for the specific event
        `;
        eventList.appendChild(li);  // Add the event to the list in the DOM
      });
    });

  // Handle ticket booking if a booking form is present
  const bookingForm = document.getElementById('booking-form');
  if (bookingForm) {
    // Add an event listener to handle form submission
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();  // Prevent the default form submission behavior

      const tickets = document.getElementById('tickets').value;  // Get the number of tickets from the form
      const userId = 1;  // Example user ID (replace with dynamic value if necessary)
      const eventId = 1;  // Example event ID (replace with dynamic value if necessary)

      // Send a POST request to book tickets for the event
      fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },  // Set the request content type to JSON
        body: JSON.stringify({ user_id: userId, event_id: eventId, tickets: tickets })  // Send the booking data as a JSON object
      })
      .then(response => response.json())  // Parse the response as JSON
      .then(data => alert(data.message));  // Display the response message in an alert
    });
  }

  // Fetch user profile data and display it on the page
  const userId = 1;  // Example user ID (replace with dynamic value if necessary)
  fetch(`/api/profile/${userId}`)
    .then(response => response.json())  // Parse the response as JSON
    .then(user => {
      // Display the user's profile information on the page
      document.getElementById('user-name').textContent = user.name;
      document.getElementById('user-email').textContent = user.email;
      document.getElementById('user-dob').textContent = user.dob;
      document.getElementById('user-bio').textContent = user.bio;
    });
});
