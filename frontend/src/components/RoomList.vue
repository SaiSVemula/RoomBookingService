<!-- RoomList.vue -->
<template>
    <div>
      <h2 class="mb-4">Available Rooms</h2>
      <div v-if="rooms.length === 0" class="alert alert-info">No rooms available.</div>
      <div v-else class="row">
        <RoomCard
          v-for="room in rooms"
          :key="room.id"
          :room="room"
          @select="selectRoom"
        />
      </div>
    </div>
  </template>
  
  <script>
  import RoomCard from './RoomCard.vue'
  
  export default {
    components: { RoomCard },
    props: {
      rooms: {
        type: Array,
        required: true,
        default: () => [], // Set a default empty array to prevent undefined errors
      },
    },
    methods: {
      selectRoom(room) {
        this.$emit('selectRoom', room)
      },
    },
  }
  </script>
  
  <style scoped>
  /* Styles specific to RoomList */
  </style>
  