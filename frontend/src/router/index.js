import { createRouter, createWebHistory } from 'vue-router'
import RoomList from '../components/RoomList.vue'
import RoomDetails from '../components/RoomDetails.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: RoomList,
    },
    {
        path: '/room/:id',
        name: 'RoomDetails',
        component: RoomDetails,
        props: true,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
