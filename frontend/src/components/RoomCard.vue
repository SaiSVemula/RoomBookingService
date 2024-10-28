<!-- RoomCard.vue -->
<template>
    <div class="col-md-4 mb-3">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ room.name }}</h5>
          <p class="card-text">Capacity: {{ room.capacity }}</p>
          <button class="btn btn-primary" @click="selectRoom">
            Check Availability
          </button>
        </div>
      </div>
    </div>
</template>
  
<script>
  export default {
    name: 'RoomCard',
    props: {
      room: {
        type: Object,
        required: true,
      },
    },
    methods: {
      selectRoom() {
        // Emit the room object up to RoomList.vue
        this.$emit('select', this.room)
      },
    },
  }
</script>
  