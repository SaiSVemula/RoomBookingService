<template>
    <div>
        <h2>Testing the CRUD methods</h2>
        <button @click="testGetRooms">Test GET</button>
        <button @click="testCreateBooking">Test POST</button>
        <button @click="testUpdateBooking(1)">Test PUT</button> //pass the booking id
        <button @click="testDeleteBooking(1)">Test DELETE</button> //pass the booking id
    </div>
</template>

<script>
    export default {
        methods: {
            testGetRooms(){
                fetch('/rooms/')
                .then(response => response.json())
                .then(data => console.log('GET request successful: ', data))
                .catch(error => console.error('Error with GET:', error));
            },

            testCreateBooking(){
                const newBooking = {
                    user_id: 1,
                    room_id: 1,
                    start_datetime: '2024-10-25T10:00:00',
                    end_datetime: '2024-10-25T11:00:00',
                };


                fetch('/bookings/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(newBooking), // body data type must match "Content-Type" header
                })

                .then(response => response.json())
                .then(data => console.log('POST request successful: ', data))
                .catch(error => console.error('Error with POST:', error));
            },


            testUpdateBooking(bookingId){
                const updatedBooking = {
                    user_id: 1,
                    room_id: 1,
                    start_datetime: '2024-10-25T10:00:00',
                    end_datetime: '2024-10-25T12:00:00',
                };

                fetch('/bookings/${bookingId}/update/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(updatedBooking), // body data type must match "Content-Type" header
                })

                .then(response => response.json())
                .then(data => console.log('PUT request successful: ', data))
                .catch(error => console.error('Error with PUT:', error));
            },

            testDeleteBooking(bookingId){
                fetch('/bookings/${bookingId}/delete/', {
                    method: 'DELETE',
                })

                .then(response => response.json())
                .then(data => console.log('DELETE request successful: ', data))
                .catch(error => console.error('Error with DELETE:', error));
            }
        }
    }
</script>