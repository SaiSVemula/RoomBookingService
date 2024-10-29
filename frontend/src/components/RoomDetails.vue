<template>
    <div class="container mt-4">
        <h2>{{ room.name }}</h2>
        <p>Capacity: {{ room.capacity }}</p>
        <h3>Available Time Slots</h3>
        <div class="timeslot-grid">
            <button v-for="slot in availableSlots" :key="slot" class="btn btn-outline-primary m-2"
                @click="selectSlot(slot)">
                {{ slot }}
            </button>
        </div>
        <button v-if="selectedSlots.length" class="btn btn-primary mt-4" @click="confirmBooking">
            Confirm Booking
        </button>
    </div>
</template>

<script>
export default {
    name: 'RoomDetails',
    props: {
        room: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            availableSlots: ['09:00', '10:00', '11:00', '12:00', '13:00'], // Placeholder slots
            selectedSlots: [],
        }
    },
    methods: {
        selectSlot(slot) {
            if (this.selectedSlots.includes(slot)) {
                this.selectedSlots = this.selectedSlots.filter((s) => s !== slot)
            } else {
                this.selectedSlots.push(slot)
            }
        },
        confirmBooking() {
            console.log('Selected slots:', this.selectedSlots)
        },
    },
}
</script>

<style scoped>
.timeslot-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
</style>