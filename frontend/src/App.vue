<template>
    <NavBar />
    <div id="app">
        <div class="container mt-4">
            <b-tabs>
                <b-tab title="Room List" active>
                    <RoomList :rooms="rooms" @selectRoom="handleRoomSelection" />
                </b-tab>
                <b-tab title="Past Bookings">
                    <PastBookingsList :bookings="userBookings" />
                </b-tab>
            </b-tabs>
        </div>
    </div>
    <FooterComp />
</template>

<script>
//used for testing not for production  
// import TestCRUD from './components/Test/TestCRUD.vue'
// import TestCRUDforms from './components/Test/TestCRUDforms.vue'
import NavBar from './components/static/NavBar.vue'
import Footer from './components/static/Footer.vue'
import RoomList from './components/RoomList.vue'
import PastBookingsList from './components/PastBookingsList.vue'

// const baseUrl = 'http://localhost:8000/api/'

export default {
    components: {
        NavBar,
        Footer,
        RoomList,
        PastBookingsList,
        
    },
    data() {
        return {
            rooms: [],
            availableSlots: [],
            selectedRoom: null,
            userName: '', // Track the user name here
            userId: 1, // defaults to one 
            userBookings: [],
            users: [],
            selectedDate: new Date(),
            selectedBooking: null,
            updatedBooking: null,
        }
    },
    created() {
        const userEmail = this.getCookie('userEmail');
        const userId = this.getCookie('userId');
        if (!userEmail || !userId) {
            this.$router.push('/');
        } else {
            // Fetch data since the user is logged in
            this.fetchRooms();
            this.fetchUserBookings();
            this.fetchUsers();
        }
    },
    methods: {
        // API functions

        // user API
        async checkUserName(name) {
            try {
                this.userName = name;
                this.fetchRooms();
                console.log(name);
                const response = await fetch(`http://localhost:8000/api/users/verify/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: name }),
                });

                if (response.ok) {
                    const data = await response.json();
                    this.userName = name;
                    this.userId = data.id; // Dynamically set userId based on response

                    this.setCookie('userName', this.userName, 1); // 1-day expiration
                    this.setCookie('userId', this.userId, 1);

                    this.fetchRooms();
                    this.fetchUserBookings();
                    this.fetchUsers();
                } else {
                    const errorData = await response.json();
                    this.userName = '';
                    alert(errorData.error); // Display error if user does not exist

                }
            } catch (error) {
                console.error("Error verifying user:", error);
                alert("An error occurred. Please try again.");
            }
        },

        // users API functions
        async fetchUsers() {
            try {
                const response = await fetch(`http://localhost:8000/api/users/`);
                const data = await response.json();
                this.users = data.users;
                console.log('Users:', this.users);
            } catch (error) {
                console.error('Failed to fetch users:', error);
            }
        },
        async createUser(newUser) {
            try {
                const response = await fetch(`http://localhost:8000/api/users/create/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newUser),
                });
                const data = await response.json();
                this.users.push(data.user);
            } catch (error) {
                console.error('Failed to create user:', error);
            }
        },
        async updateUser(updatedUser) {
            try {
                // console.log(`http://localhost:8000/api/users/${updatedUser.id}/update/`);
                const response = await fetch(`http://localhost:8000/api/users/${updatedUser.id}/update/`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedUser),
                });
                const data = await response.json();
                const index = this.users.findIndex(user => user.id === updatedUser.id);
                if (index !== -1) this.users.splice(index, 1, data.user);
            } catch (error) {
                console.error('Failed to update user:', error);
            }
        },
        async deleteUser(userId) {
            try {
                await fetch(`http://localhost:8000/api/users/${userId}/delete/`, {
                    method: 'DELETE',
                });
                this.users = this.users.filter(user => user.id !== userId);
            } catch (error) {
                console.error('Failed to delete user:', error);
            }
        },

        // rooms API functions
        async fetchRooms() {
            try {
                const response = await fetch(`http://localhost:8000/api/rooms/`);
                const data = await response.json();
                this.rooms = data;
                console.log('Rooms:', this.rooms);
            } catch (error) {
                console.error('Error fetching rooms:', error);
            }
        },
        async createRoom(newRoom) {
            try {
                const response = await fetch(`http://localhost:8000/api/rooms/create/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newRoom),
                });
                const data = await response.json();
                this.rooms.push(data.room);
            } catch (error) {
                console.error('Failed to create room:', error);
            }
        },
        async updateRoom(updatedRoom) {
            try {
                const response = await fetch(`http://localhost:8000/api/rooms/${updatedRoom.id}/update/`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedRoom),
                });
                const data = await response.json();
                const index = this.rooms.findIndex(room => room.id === updatedRoom.id);
                if (index !== -1) this.rooms.splice(index, 1, data.room);
            } catch (error) {
                console.error('Failed to update room:', error);
            }
        },
        async deleteRoom(roomId) {
            try {
                await fetch(`http://localhost:8000/api/rooms/${roomId}/delete/`, {
                    method: 'DELETE',
                });
                this.rooms = this.rooms.filter(room => room.id !== roomId);
            } catch (error) {
                console.error('Failed to delete room:', error);
            }
        },

        // available slots API functions - seperate to other APIs
        async fetchAvailableSlots(roomId) {
            try {
                const response = await fetch(`http://localhost:8000/api/available-times/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ room_id: roomId, date: this.selectedDate.toISOString().split('T')[0] })
                });
                if (!response.ok) throw new Error('Failed to fetch available slots');
                const data = await response.json();
                this.availableSlots = data.available_slots;
            } catch (error) {
                console.error('Error fetching available slots:', error);
                this.availableSlots = [];
            }
        },

        // booking API functions

        // fetches the users past bookings
        async fetchUserBookings() {
            try {
                this.currentView = 'viewBookings'; // Switch to the Bookings view
                const response = await fetch(`http://localhost:8000/api/bookings/user/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: this.userId }) // Assuming user ID is in userName for now
                });
                if (!response.ok) throw new Error('Failed to fetch bookings');
                const data = await response.json();
                this.userBookings = data.bookings || [];
                console.log('User bookings:', this.userBookings);
            } catch (error) {
                console.error('Error fetching user bookings:', error);
            }
        },
        async confirmBooking({ selectedSlots }) {
            if (selectedSlots.length === 0) {
                alert('Please select at least one slot.');
                return;
            }

            const startHour = selectedSlots[0].start;
            const endHour = selectedSlots[selectedSlots.length - 1].end;

            try {
                const response = await fetch(`http://localhost:8000/api/bookings/create/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        room_id: this.selectedRoom.id,
                        user_id: this.userId,
                        start_hour: startHour,
                        end_hour: endHour,
                        user_name: this.userName,
                    })
                });

                if (!response.ok) throw new Error('Failed to create booking');
                const data = await response.json();
                console.log(`Booking created with ID: ${data.booking_id}`);

                alert(`Booking confirmed for ${this.selectedRoom.name} from ${startHour} to ${endHour} by ${this.userName}`);
                this.selectedRoom = null;
                this.availableSlots = [];
            } catch (error) {
                console.error('Error creating booking:', error);
                alert('Failed to create booking. Please try again.');
            }
        },
        async editBooking(updatedBooking) {
            console.log('Updating booking:', updatedBooking);
            try {
                // Format hours to HH:MM format
                const formatHour = (hour) => `${hour.toString().padStart(2, '0')}:00`;

                const response = await fetch(`http://localhost:8000/api/bookings/${updatedBooking.id}/update/`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        start_hour: formatHour(updatedBooking.start_hour),
                        end_hour: formatHour(updatedBooking.end_hour),
                        status: updatedBooking.status,
                    }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Error updating booking:', errorData);
                    alert(`Failed to update booking: ${errorData.error}`);
                    return;
                }

                const data = await response.json();
                console.log('Updated booking:', data.booking);

                // Update the local list of bookings
                const index = this.userBookings.findIndex(booking => booking.id === updatedBooking.id);
                if (index !== -1) {
                    this.userBookings.splice(index, 1, data.booking);
                }
            } catch (error) {
                console.error('Failed to update booking:', error);
                alert('Failed to update booking. Please try again.');
            }
        },
        // Handle delete booking event from UserBookings.vue
        async deleteBooking(selectedBooking) {
            console.log("Deleting booking:", selectedBooking.id);
            try {
                const response = await fetch(`http://localhost:8000/api/bookings/${selectedBooking.id}/delete/`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    // alert("Booking deleted successfully");
                    this.fetchUserBookings(); // Refresh bookings after deletion
                } else {
                    console.error("Failed to delete booking");
                }
            } catch (error) {
                console.error("Error deleting booking:", error);
            }
        },
        // js functions

        // confirm the deletion before deleting the booking
        confirmDeleteBooking(selectedBooking) {
            if (confirm("Are you sure you want to delete this booking?")) {
                this.deleteBooking(selectedBooking);
            }
        },
        // Open the booking modal for the selected room
        openMakeBooking(room) {
            this.selectedRoom = room;
            this.fetchAvailableSlots(room.id);
        },
        updateSelectedDate(date) {
            // console.log(date);
            this.selectedDate = date;
            // console.log(this.selectedDate);
            if (this.selectedRoom) {
                this.fetchAvailableSlots(this.selectedRoom.id);
            }
        },
        // Handle logout: clear userName 
        logout() {
            this.userName = '';
            this.userId = '';
            this.deleteCookie('userName');
            this.deleteCookie('userId');
        },
        closeMakeBooking() {
            this.selectedRoom = null;
            this.availableSlots = [];
        },
        // Cookie helper functions
        setCookie(name, value, days) {
            const date = new Date();
            date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
            document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
        },
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
            return '';
        },
        deleteCookie(name) {
            document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
        },

    },
}
</script>