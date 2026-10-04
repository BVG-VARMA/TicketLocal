<template>
  <div class="min-h-screen pb-20 pt-10 px-4 lg:px-8 flex items-center justify-center">
    <div v-if="loading" class="text-center py-20">
      <div class="w-12 h-12 border-4 border-[#F84464] border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p class="text-sm font-semibold text-slate-400 mt-4">Loading your confirmed pass...</p>
    </div>

    <div v-else-if="booking" class="max-w-xl w-full">
      <!-- Success Badge Header -->
      <div class="text-center mb-8 animate-in fade-in zoom-in duration-500">
        <div class="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-3xl mx-auto shadow-2xl shadow-emerald-500/30">
          ✓
        </div>
        <h1 class="text-2xl sm:text-3xl font-black text-white mt-4 tracking-tight">
          Booking Confirmed!
        </h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">
          Your digital QR ticket has been minted and stored locally.
        </p>
      </div>

      <!-- Ticket Card -->
      <div class="bms-card rounded-3xl overflow-hidden border border-white/15 shadow-2xl relative">
        <!-- Top ticket header -->
        <div class="p-6 bg-gradient-to-r from-rose-950/40 via-purple-950/30 to-slate-900 border-b border-white/10 flex items-start justify-between">
          <div>
            <div class="text-[10px] uppercase font-bold tracking-widest text-[#F84464]">
              Verified Cinema Pass
            </div>
            <h2 class="text-xl font-extrabold text-white mt-1">
              {{ booking.content_title }}
            </h2>
            <div class="text-xs text-slate-300 mt-1 flex items-center gap-2">
              <span>🏛️ {{ booking.theater_name }}</span>
              <span>•</span>
              <span>{{ booking.screen_name }}</span>
            </div>
          </div>
          <div class="text-right">
            <div class="text-[10px] text-slate-400 uppercase font-bold">Booking #</div>
            <div class="text-sm font-mono font-bold text-white">#{{ booking.id }}</div>
          </div>
        </div>

        <!-- Middle Ticket Body -->
        <div class="p-6 space-y-5">
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 pb-4 border-b border-white/10 text-xs">
            <div>
              <div class="text-slate-400 font-medium">Showtime</div>
              <div class="text-white font-bold mt-0.5">{{ formatDateTime(booking.start_time) }}</div>
            </div>
            <div>
              <div class="text-slate-400 font-medium">Seats</div>
              <div class="text-[#F84464] font-bold font-mono mt-0.5">
                {{ booking.seats.map((s) => `${s.row_label}${s.seat_number}`).join(', ') }}
              </div>
            </div>
            <div>
              <div class="text-slate-400 font-medium">Amount Paid</div>
              <div class="text-emerald-400 font-bold font-mono mt-0.5">₹{{ booking.total.toFixed(2) }}</div>
            </div>
          </div>

          <!-- QR Code Ticket Image Preview -->
          <div v-if="booking.ticket" class="flex flex-col items-center justify-center p-4 rounded-2xl bg-black/40 border border-white/10">
            <div class="w-48 h-48 rounded-xl overflow-hidden shadow-xl border border-white/10 bg-white p-2">
              <img
                :src="booking.ticket.qr_url"
                alt="Ticket QR Code"
                class="w-full h-full object-contain"
              />
            </div>
            <div class="text-[11px] font-mono text-slate-400 mt-3 text-center">
              Scan at cinema gate for instant paperless admission
            </div>

            <a
              :href="booking.ticket.qr_url"
              download
              class="mt-3 px-4 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 border border-white/15 text-xs font-bold text-white transition-all inline-flex items-center gap-1.5"
            >
              <span>📥</span>
              <span>Download Ticket PNG</span>
            </a>
          </div>
        </div>

        <!-- Card Footer -->
        <div class="p-4 bg-white/5 border-t border-white/10 flex items-center justify-between gap-3">
          <router-link
            to="/bookings"
            class="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-slate-200 text-xs font-bold transition-all"
          >
            My Bookings
          </router-link>
          <router-link
            to="/"
            class="px-5 py-2 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white text-xs font-bold shadow-md shadow-[#F84464]/30 transition-all"
          >
            Book More Movies
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import confetti from 'canvas-confetti'
import apiClient from '../api/client'

const route = useRoute()
const bookingId = parseInt(route.params.bookingId)
const booking = ref(null)
const loading = ref(true)

async function fetchBooking() {
  loading.value = true
  try {
    const resp = await apiClient.get(`/bookings/${bookingId}`)
    booking.value = resp.data
    triggerConfetti()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function triggerConfetti() {
  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 },
    colors: ['#F84464', '#10B981', '#F59E0B', '#3B82F6', '#EC4899'],
  })
}

function formatDateTime(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return d.toLocaleString([], {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  fetchBooking()
})
</script>
