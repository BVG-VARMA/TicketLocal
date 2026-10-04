<template>
  <div class="min-h-screen pb-32">
    <!-- Header Bar -->
    <div class="bg-[#181A24] border-b border-white/10 px-4 lg:px-8 py-4 sticky top-[61px] z-20 backdrop-blur-md">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 text-xs font-semibold text-[#F84464] uppercase tracking-wider">
            <span>{{ matrix?.theater_name }}</span>
            <span>•</span>
            <span class="text-slate-300">{{ matrix?.screen_name }}</span>
          </div>
          <h1 class="text-xl font-extrabold text-white mt-0.5">
            {{ matrix?.content_title }}
          </h1>
          <div class="text-xs text-slate-400 mt-0.5">
            {{ formatDateTime(matrix?.start_time) }}
          </div>
        </div>

        <!-- Timer / Hold Status Banner -->
        <div v-if="bookingStore.holdsConfirmed" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 animate-pulse">
          <span class="text-lg">⏳</span>
          <div>
            <div class="text-[10px] uppercase font-bold tracking-wider text-amber-400">Seats Locked (10m TTL)</div>
            <div class="text-base font-black font-mono">{{ bookingStore.formattedTimer }}</div>
          </div>
        </div>

        <div v-else class="flex items-center gap-2">
          <span class="text-xs text-slate-400">Max 6 seats per booking</span>
        </div>
      </div>
    </div>

    <!-- Seating Layout & SVG Map -->
    <div class="max-w-7xl mx-auto px-4 lg:px-8 mt-8">
      <div v-if="loading" class="flex flex-col items-center justify-center py-20">
        <div class="w-12 h-12 border-4 border-[#F84464] border-t-transparent rounded-full animate-spin"></div>
        <p class="text-sm font-semibold text-slate-400 mt-4">Generating live cinema layout...</p>
      </div>

      <div v-else-if="matrix" class="flex flex-col items-center">
        <!-- SVG Seat Map -->
        <SeatMapSVG
          :rows="matrix.rows"
          :selected-seat-ids="bookingStore.selectedSeatIds"
          @toggle-seat="bookingStore.toggleSeatSelection"
        />
      </div>
    </div>

    <!-- Fixed Bottom Summary & Action Bar -->
    <div class="fixed bottom-0 left-0 right-0 z-30 bg-[#14151E]/95 backdrop-blur-xl border-t border-white/10 px-4 lg:px-8 py-4 shadow-2xl">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <!-- Selected seats info -->
        <div class="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-start">
          <div>
            <div class="text-xs text-slate-400 font-semibold">
              Selected Seats ({{ bookingStore.selectedSeats.length }}/6):
            </div>
            <div class="flex flex-wrap items-center gap-1.5 mt-1">
              <span
                v-for="s in bookingStore.selectedSeats"
                :key="s.id"
                class="px-2 py-0.5 rounded bg-[#F84464]/20 border border-[#F84464]/50 text-white text-xs font-mono font-bold"
              >
                {{ s.row_label }}{{ s.seat_number }}
              </span>
              <span v-if="bookingStore.selectedSeats.length === 0" class="text-xs text-slate-500 italic">
                None selected yet
              </span>
            </div>
          </div>

          <div class="sm:pl-6 sm:border-l sm:border-white/10 text-right sm:text-left">
            <div class="text-xs text-slate-400 font-semibold">Estimated Subtotal:</div>
            <div class="text-xl font-black text-white">
              ₹{{ bookingStore.subtotal.toFixed(2) }}
            </div>
          </div>
        </div>

        <!-- Action Button -->
        <div class="flex items-center gap-3 w-full sm:w-auto">
          <button
            v-if="bookingStore.holdsConfirmed"
            @click="proceedToCheckout"
            class="w-full sm:w-auto px-8 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-sm shadow-lg shadow-emerald-500/30 transition-all hover:scale-105 active:scale-95"
          >
            Proceed to Checkout →
          </button>
          <button
            v-else
            @click="handleHoldSeats"
            :disabled="bookingStore.selectedSeats.length === 0 || bookingStore.isHolding"
            class="w-full sm:w-auto px-8 py-3 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white font-bold text-sm shadow-lg shadow-[#F84464]/30 transition-all hover:scale-105 active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
          >
            <span v-if="bookingStore.isHolding">Acquiring Redis Lock...</span>
            <span v-else>Lock Seats & Proceed (10m Hold)</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SeatMapSVG from '../components/SeatMapSVG.vue'
import { useBookingStore } from '../stores/booking'

const route = useRoute()
const router = useRouter()
const bookingStore = useBookingStore()

const showId = parseInt(route.params.id)
const matrix = ref(null)
const loading = ref(true)
let pollTimer = null

async function loadMatrix() {
  try {
    const data = await bookingStore.fetchSeatMatrix(showId)
    matrix.value = data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function handleHoldSeats() {
  const success = await bookingStore.holdSelectedSeats(showId)
  if (success) {
    router.push(`/checkout/${showId}`)
  }
}

function proceedToCheckout() {
  router.push(`/checkout/${showId}`)
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

onMounted(async () => {
  bookingStore.clearTimer()
  bookingStore.selectedSeats = []
  bookingStore.holdsConfirmed = false
  await loadMatrix()

  // Poll matrix every 5 seconds to reflect live seat changes
  pollTimer = setInterval(async () => {
    if (!bookingStore.isHolding) {
      await loadMatrix()
    }
  }, 5000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>
