<template>
    <div>
        <h2>Testing CRUD Operations</h2>

        <button @click="getRooms">Test GET Rooms</button>
        <button @click="getBookings">Test GET Bookings</button>
        <button @click="getUsers">Test GET Users</button>

        <!-- Display Rooms -->
        <div v-if="rooms.length">
            <h3>Rooms:</h3>
            <ul>
                <li v-for="room in rooms" :key="room.id">{{ room.name }}</li>
            </ul>
        </div>

        <!-- Display Bookings -->
        <div v-if="bookings.length">
            <h3>Bookings:</h3>
            <ul>
                <li v-for="booking in bookings" :key="booking.id">
                    {{ booking.user_id }} - {{ booking.room_id }} - {{ booking.start_hour }} to {{ booking.end_hour }}
                </li>
            </ul>
        </div>

        <!-- Display Users -->
        <div v-if="users.length">
            <h3>Users:</h3>
            <ul>
                <li v-for="user in users" :key="user.id">{{ user.name }} - {{ user.email }}</li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    props: ['getRooms', 'getBookings', 'getUsers', 'rooms', 'bookings', 'users']
}
</script>
