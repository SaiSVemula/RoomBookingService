<template>
  <div class="col-md-4 mb-3">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ room.name }}</h5>
        <p class="card-text">Capacity: {{ room.capacity }}</p>
        <router-link
          :to="{ name: 'RoomDetails', params: { id: room.id, room: room } }"
          class="btn btn-primary"
        >
          Check Availability
        </router-link>
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
}
</script>
