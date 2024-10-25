<template>
    <div>
        <h2>Testing CRUD Operations for Bookings</h2>

        <!-- Buttons to test each CRUD function manually -->
        <button @click="testGetRooms()">Test GET Rooms</button>
        <button @click="testGetBookings()">Test GET Bookings</button>
        <button @click="testCreateBooking()">Test POST Booking</button>
        <button @click="testUpdateBooking(1)">Test PUT Booking (ID: 1)</button>
        <button @click="testDeleteBooking(1)">Test DELETE Booking (ID: 1)</button>

        <!-- Display fetched booking data -->
        <div v-if="bookings.length" class="booking-list">
            <h3>Fetched Bookings:</h3>
            <ul>
                <li v-for="booking in bookings" :key="booking.id">
                    <strong>User:</strong> {{ booking.user.name }} <br>
                    <strong>Room:</strong> {{ booking.room.name }} <br>
                    <strong>Start Hour:</strong> {{ booking.start_hour }} <br>
                    <strong>End Hour:</strong> {{ booking.end_hour }} <br>
                    <strong>Status:</strong> {{ booking.status }} <br>
                    <strong>Date:</strong> {{ booking.booking_date }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            bookings: [],  // Store fetched bookings data
        };
    },
    methods: {
        // READ (GET request to fetch rooms)
        testGetRooms() {
            fetch('http://localhost:8000/api/rooms/')
                .then(response => response.json())
                .then(data => {
                    console.log('GET Rooms:', data);
                })
                .catch(error => console.error('Error with GET rooms request:', error));
        },

        // READ (GET request to fetch bookings)
        testGetBookings() {
            fetch('http://localhost:8000/api/bookings/')
                .then(response => response.json())
                .then(data => {
                    console.log('GET Bookings:', data);
                    this.bookings = data; // Store bookings data in component's data
                })
                .catch(error => console.error('Error with GET bookings request:', error));
        },

        // CREATE (POST request to create a new booking)
        testCreateBooking() {
            const newBooking = {
                user_id: 1,  // Replace with a valid user ID
                room_id: 1,  // Replace with a valid room ID
                start_hour: '14:00:00',  // Ensure correct time format (HH:MM:SS)
                end_hour: '15:00:00',    // Set to an hour after start_hour
                status: 'Pending'
            };

            fetch('http://localhost:8000/api/bookings/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newBooking),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('POST Booking:', data);
                })
                .catch(error => console.error('Error with POST booking request:', error));
        },

        // UPDATE (PUT request to update a booking)
        testUpdateBooking(bookingId) {
            const updatedBooking = {
                start_hour: '15:00:00',  // Ensure correct time format (HH:MM:SS)
                end_hour: '16:00:00',    // Updated end_hour, ensure format (HH:MM:SS)
                status: 'Confirmed'
            };

            fetch(`http://localhost:8000/api/bookings/${bookingId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedBooking),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('PUT Booking:', data);
                })
                .catch(error => console.error('Error with PUT booking request:', error));
        },

        // DELETE (DELETE request to remove a booking)
        testDeleteBooking(bookingId) {
            fetch(`http://localhost:8000/api/bookings/${bookingId}/delete/`, {
                method: 'DELETE',
            })
                .then(response => response.json())
                .then(data => {
                    console.log('DELETE Booking:', data);
                })
                .catch(error => console.error('Error with DELETE booking request:', error));
        },
    },
};
</script>

<style scoped>
.booking-list {
    margin-top: 20px;
}
</style>