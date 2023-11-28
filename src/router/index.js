import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Register from '../views/register.vue'
import Login from '../views/login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import CreateTheatre from '../views/CreateTheatre.vue'
import EditTheatre from '../views/EditTheatre.vue'
import ViewTheatre from '../views/ViewTheatre.vue'
import CreateShow from '../views/CreateShow.vue'
import EditShow from '../views/EditShow.vue'
import UserTheatres from '../views/UserTheatres.vue'
import BookTicket from '../views/BookTicket.vue'
import ViewBookings from '../views/ViewBookings.vue'
import UserTheatreInfo from '../views/UserTheatreInfo.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/admin/createTheatre',
    name: 'CreateTheatre',
    component: CreateTheatre
  },
  {
    path: '/admin/:id/editTheatre',
    name: 'EditTheatre',
    component: EditTheatre
  },
  {
    path: '/admin/:id/:theatreName/viewShows',
    name: 'ViewTheatre',
    component: ViewTheatre
  },
  {
    path: '/admin/:theatre_id/:theatreName/createShow',
    name: 'CreateShow',
    component: CreateShow
  },
  {
    path: '/admin/:theatre_id/:theatreName/:show_id/editShow',
    name: 'EditShow',
    component: EditShow
  },
  {
    path: '/user/:id/:username/dashboard',
    name: 'UserDashboard',
    component: UserDashboard
  },
  {
    path: '/user/:id/:username/theatres',
    name: 'UserTheatres',
    component: UserTheatres
  },
  {
    path: '/user/:id/:username/theatre/:theatre_id',
    name: 'UserTheatreInfo',
    component: UserTheatreInfo
  },
  {
    path: '/user/:id/:username/:show_id/:show_name/book',
    name: 'BookTicket',
    component: BookTicket
  },
  {
    path: '/user/:id/:username/bookings',
    name: 'ViewBookings',
    component: ViewBookings
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
