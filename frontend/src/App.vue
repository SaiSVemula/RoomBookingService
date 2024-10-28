<!-- App.vue -->
<template>
    <NavBar />
    <div id="app">
      <div class="container mt-4">
        <RoomList :rooms="rooms" @selectRoom="handleRoomSelection" /> <!-- Listen for the 'selectRoom' event from RoomList -->
      </div>
    </div> 
    <FooterComp />
</template>
  
<script>
//used for testing not for production  
// import TestCRUD from './components/Test/TestCRUD.vue'
// import TestCRUDforms from './components/Test/TestCRUDforms.vue'
import NavBar from './components/static/NavBar.vue'
import FooterComp from './components/static/FooterComp.vue'
import RoomList from './components/RoomList.vue'

const baseUrl = 'http://localhost:8000'

export default {
    components: {
        NavBar,
        FooterComp,
        RoomList,
    },
    data() {
      return {
          rooms: [],
            selectedRoom: null,
          bookings: [],
          users: [],
        }
    },
    created() {
        this.fetchRooms()
    },
    methods: {
        //#region Event Handlers
        handleRoomSelection(rooms) {
            this.selectedRoom = rooms
            console.log('Selected room:', rooms)
        },
        //#endregion

        //#region API Fetch 
        // Room CRUD methods
        async fetchRooms() {
            try {
                const response = await fetch(`${baseUrl}/api/rooms/`)
                this.rooms = await response.json()
                console.log('Rooms:', this.rooms)
            } catch (error) {
                console.error('Error fetching rooms:', error)
            }
        },
        async createRoom(newRoom) {
            try {
                const response = await fetch(`${baseUrl}/api/rooms/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newRoom)
                })
                const room = await response.json()
                this.rooms.push(room)
            } catch (error) {
                console.error('Error creating room:', error)
            }
        },
        // Booking CRUD methods
        async getBookings() {
            try {
                const response = await fetch(`${baseUrl}/api/bookings/`)
                this.bookings = await response.json()
            } catch (error) {
                console.error('Error fetching bookings:', error)
            }
        },
        async createBooking(newBooking) {
            try {
                const response = await fetch(`${baseUrl}/api/bookings/create/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newBooking)
                })
                const booking = await response.json()
                this.bookings.push(booking)
            } catch (error) {
                console.error('Error creating booking:', error)
            }
        },
        async updateBooking(bookingId, updatedBooking) {
            try {
                const response = await fetch(`${baseUrl}/api/bookings/${bookingId}/update/`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedBooking)
                })
                console.log('Updated Booking:', await response.json())
            } catch (error) {
                console.error('Error updating booking:', error)
            }
        },
        async deleteBooking(bookingId) {
            try {
                await fetch(`${baseUrl}/api/bookings/${bookingId}/delete/`, { method: 'DELETE' })
                this.bookings = this.bookings.filter(b => b.id !== bookingId)
            } catch (error) {
                console.error('Error deleting booking:', error)
            }
        },
        // User CRUD methods
        async getUsers() {
            try {
                const response = await fetch(`${baseUrl}/api/users/`)
                this.users = await response.json()
            } catch (error) {
                console.error('Error fetching users:', error)
            }
        },
        async createUser(newUser) {
            try {
                const response = await fetch(`${baseUrl}/api/users/create/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newUser)
                })
                const user = await response.json()
                this.users.push(user)
            } catch (error) {
                console.error('Error creating user:', error)
            }
        },
        async updateUser(userId, updatedUser) {
            try {
                const response = await fetch(`${baseUrl}/api/users/${userId}/update/`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedUser)
                })
                console.log('Updated User:', await response.json())
            } catch (error) {
                console.error('Error updating user:', error)
            }
        },
        async deleteUser(userId) {
            try {
                await fetch(`${baseUrl}/api/users/${userId}/delete/`, { method: 'DELETE' })
                this.users = this.users.filter(u => u.id !== userId)
            } catch (error) {
                console.error('Error deleting user:', error)
            }
        }
        //#endregion
    }
}
</script>
