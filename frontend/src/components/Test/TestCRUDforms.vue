<template>
    <div>
        <h2>Testing CRUD Forms</h2>

        <!-- Create Booking Form -->
        <div>
            <h3>Create Booking</h3>
            <form @submit.prevent="createBooking(newBooking)">
                <input v-model="newBooking.user_id" placeholder="User ID" />
                <input v-model="newBooking.room_id" placeholder="Room ID" />
                <input v-model="newBooking.start_hour" placeholder="Start Hour (HH:MM:SS)" />
                <input v-model="newBooking.end_hour" placeholder="End Hour (HH:MM:SS)" />
                <input v-model="newBooking.status" placeholder="Status" />
                <button type="submit">Create Booking</button>
            </form>
        </div>

        <!-- Update Booking Form -->
        <div>
            <h3>Update Booking</h3>
            <form @submit.prevent="updateBooking(updateBookingData.id, updateBookingData)">
                <input v-model="updateBookingData.id" placeholder="Booking ID" />
                <input v-model="updateBookingData.start_hour" placeholder="Start Hour (HH:MM:SS)" />
                <input v-model="updateBookingData.end_hour" placeholder="End Hour (HH:MM:SS)" />
                <input v-model="updateBookingData.status" placeholder="Status" />
                <button type="submit">Update Booking</button>
            </form>
        </div>

        <!-- Create User Form -->
        <div>
            <h3>Create User</h3>
            <form @submit.prevent="createUser(newUser)">
                <input v-model="newUser.name" placeholder="Name" />
                <input v-model="newUser.email" placeholder="Email" />
                <button type="submit">Create User</button>
            </form>
        </div>

        <!-- Update User Form -->
        <div>
            <h3>Update User</h3>
            <form @submit.prevent="updateUser(updateUserData.id, updateUserData)">
                <input v-model="updateUserData.id" placeholder="User ID" />
                <input v-model="updateUserData.name" placeholder="Name" />
                <input v-model="updateUserData.email" placeholder="Email" />
                <button type="submit">Update User</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    props: ['createBooking', 'createUser', 'updateBooking', 'deleteBooking', 'updateUser', 'deleteUser'],
    data() {
        return {
            newBooking: { user_id: '', room_id: '', start_hour: '', end_hour: '', status: '' },
            updateBookingData: { id: '', start_hour: '', end_hour: '', status: '' },
            newUser: { name: '', email: '' },
            updateUserData: { id: '', name: '', email: '' }
        };
    }
};
</script>

<style scoped>
form {
    margin: 10px 0;
    display: flex;
    flex-direction: column;
    max-width: 300px;
}
form input {
    margin-bottom: 10px;
    padding: 5px;
}
form button {
    padding: 5px;
}
</style>
