import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ContentDetailView from '../views/ContentDetailView.vue'
import SeatSelectionView from '../views/SeatSelectionView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import BookingConfirmationView from '../views/BookingConfirmationView.vue'
import MyBookingsView from '../views/MyBookingsView.vue'
import ChaosLabView from '../views/ChaosLabView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/content/:id',
    name: 'content-detail',
    component: ContentDetailView,
  },
  {
    path: '/shows/:id/seats',
    name: 'seat-selection',
    component: SeatSelectionView,
  },
  {
    path: '/checkout/:showId',
    name: 'checkout',
    component: CheckoutView,
  },
  {
    path: '/confirmation/:bookingId',
    name: 'confirmation',
    component: BookingConfirmationView,
  },
  {
    path: '/bookings',
    name: 'my-bookings',
    component: MyBookingsView,
  },
  {
    path: '/chaos',
    name: 'chaos-lab',
    component: ChaosLabView,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
