<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 overflow-y-auto bg-black/95 backdrop-blur-md">
    <div class="bg-[#161822] w-full max-w-5xl rounded-3xl border border-slate-700/80 shadow-2xl overflow-hidden flex flex-col max-h-[96vh]">
      
      <!-- STAGE 1: BookMyShow "How Many Seats?" Step (BMS Signature Quantity Modal) -->
      <div v-if="step === 'quantity'" class="p-6 sm:p-8 space-y-6 animate-in zoom-in-95 duration-200">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <span class="text-xs font-black uppercase tracking-wider text-[#F84464]">BookMyShow Experience</span>
            <h2 class="text-xl sm:text-2xl font-black text-white mt-0.5">How Many Seats?</h2>
            <p class="text-xs text-slate-400 mt-1">
              {{ show.movie?.title }} • {{ show.theater?.name }} ({{ show.format }})
            </p>
          </div>
          <button 
            @click="$emit('close')"
            class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors cursor-pointer"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Vehicle Quantity Selector Grid (Iconic BMS Style) -->
        <div class="py-4">
          <div class="flex items-center justify-center mb-6">
            <div class="text-center p-4 rounded-3xl bg-[#222434]/80 border border-slate-700/80 shadow-inner max-w-xs w-full">
              <span class="text-4xl block mb-2">{{ activeVehicle.icon }}</span>
              <span class="text-xs font-black uppercase text-[#F84464] tracking-wider">{{ activeVehicle.label }}</span>
              <h3 class="text-lg font-black text-white mt-0.5">{{ selectedQuantity }} {{ selectedQuantity === 1 ? 'Ticket' : 'Tickets' }}</h3>
            </div>
          </div>

          <!-- Quantity Pills -->
          <div class="flex flex-wrap items-center justify-center gap-2 sm:gap-3 max-w-xl mx-auto">
            <button
              v-for="qty in seatQuantities"
              :key="qty.count"
              @click="selectedQuantity = qty.count"
              class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl font-black text-sm transition-all duration-200 cursor-pointer flex flex-col items-center justify-center"
              :class="selectedQuantity === qty.count ? 'bg-[#F84464] text-white shadow-lg shadow-[#F84464]/40 scale-110 border-2 border-white' : 'bg-[#222434] text-slate-300 hover:bg-slate-800 hover:text-white border border-slate-700'"
            >
              <span>{{ qty.count }}</span>
            </button>
          </div>
        </div>

        <!-- Price Tiers Overview -->
        <div class="border-t border-slate-800 pt-6">
          <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider text-center mb-3">Available Seat Categories</h4>
          <div class="grid grid-cols-3 gap-3 max-w-lg mx-auto text-center text-xs">
            <div class="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300">
              <span class="block text-[10px] font-black uppercase">RECLINER</span>
              <span class="text-base font-black text-white">₹350.00</span>
              <span class="text-[10px] text-slate-400 block mt-0.5">Filling Fast</span>
            </div>
            <div class="p-3 rounded-2xl bg-[#F84464]/10 border border-[#F84464]/30 text-rose-300">
              <span class="block text-[10px] font-black uppercase">PRIME</span>
              <span class="text-base font-black text-white">₹220.00</span>
              <span class="text-[10px] text-emerald-400 block mt-0.5">Available</span>
            </div>
            <div class="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-300">
              <span class="block text-[10px] font-black uppercase">CLASSIC</span>
              <span class="text-base font-black text-white">₹150.00</span>
              <span class="text-[10px] text-emerald-400 block mt-0.5">Available</span>
            </div>
          </div>
        </div>

        <!-- Select Seats CTA Button -->
        <div class="pt-2 text-center">
          <button
            @click="step = 'map'"
            class="w-full sm:w-80 py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-black text-sm shadow-xl shadow-[#F84464]/30 transition-all transform hover:-translate-y-0.5 cursor-pointer inline-flex items-center justify-center gap-2"
          >
            <span>Select {{ selectedQuantity }} {{ selectedQuantity === 1 ? 'Seat' : 'Seats' }}</span>
            <ChevronRight class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- STAGE 2: BookMyShow Interactive Seat Map Layout -->
      <div v-else class="flex flex-col h-full overflow-hidden">
        
        <!-- Modal Top Bar (BMS Cinema Specs & Timer) -->
        <div class="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between gap-4 bg-[#1e202d]">
          <div>
            <div class="flex items-center gap-2.5">
              <h2 class="text-base sm:text-lg font-black text-white">{{ show.movie?.title }}</h2>
              <span class="px-2 py-0.5 rounded bg-[#F84464]/20 border border-[#F84464]/40 text-[10px] font-black text-[#F84464] uppercase">
                {{ show.format }}
              </span>
              <button 
                @click="step = 'quantity'"
                class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-[11px] text-slate-300 font-bold border border-slate-700 flex items-center gap-1 cursor-pointer transition-colors"
                title="Change ticket quantity"
              >
                <span>{{ selectedQuantity }} {{ selectedQuantity === 1 ? 'Ticket' : 'Tickets' }}</span>
                <Edit2 class="w-3 h-3 text-[#F84464]" />
              </button>
            </div>
            <p class="text-xs text-slate-400 mt-0.5">
              {{ show.theater?.name }} • {{ show.show_date }} @ <span class="text-white font-semibold">{{ show.start_time }}</span>
            </p>
          </div>

          <!-- Timer & Close Action -->
          <div class="flex items-center gap-3 sm:gap-4">
            <!-- 10-Minute Hold Countdown Timer -->
            <div v-if="selectedSeatIds.length > 0" class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-500/15 border border-amber-500/40 text-amber-400 text-xs font-mono font-bold animate-pulse">
              <Clock class="w-4 h-4" />
              <span>Expires in: {{ formattedTimer }}</span>
            </div>

            <button 
              @click="$emit('close')"
              class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors cursor-pointer"
            >
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Main Matrix Body -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 no-scrollbar">
          
          <!-- Seat Legend (BMS Style) -->
          <div class="flex flex-wrap items-center justify-center gap-5 sm:gap-8 text-xs text-slate-300 bg-[#202230]/70 p-3 rounded-2xl border border-slate-800 select-none">
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-md bg-slate-800 border border-slate-600"></span>
              <span>Available</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-md bg-[#1EA83C] border border-[#16A34A] shadow"></span>
              <span class="font-bold text-emerald-400">Selected</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-md bg-amber-500 border border-amber-300 animate-pulse"></span>
              <span>Held (600s TTL)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-5 h-5 rounded-md bg-slate-900 border border-slate-800 text-slate-600 flex items-center justify-center font-bold text-[10px]">✕</span>
              <span>Sold</span>
            </div>
          </div>

          <!-- Alert Banner on Collision (HTTP 423) -->
          <div v-if="collisionError" class="p-3.5 rounded-2xl bg-rose-950/90 border border-rose-500 text-rose-200 text-xs flex items-center justify-between gap-3 animate-in fade-in">
            <div class="flex items-center gap-2">
              <AlertTriangle class="w-4 h-4 text-rose-400 shrink-0" />
              <span>{{ collisionError }}</span>
            </div>
            <button @click="collisionError = ''" class="text-rose-400 hover:text-white font-bold text-xs cursor-pointer">Dismiss</button>
          </div>

          <!-- Loading state -->
          <div v-if="loadingMatrix" class="py-16 text-center text-slate-400 text-sm">
            <div class="w-8 h-8 border-2 border-[#F84464] border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
            Syncing BookMyShow cinema seat layout...
          </div>

          <!-- 2D BookMyShow Seat Matrix Layout with Realistic Aisles -->
          <div v-else-if="matrix" class="space-y-6 max-w-4xl mx-auto select-none py-2">
            <div 
              v-for="group in categorizedRows" 
              :key="group.category" 
              class="space-y-3"
            >
              <!-- Category Header (e.g. ROYAL RECLINER - Rs. 350.00) -->
              <div class="flex items-center justify-between text-xs font-black text-slate-300 border-b border-slate-800/80 pb-1.5 uppercase tracking-wider">
                <span class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full" :class="group.category === 'RECLINER' ? 'bg-amber-400' : group.category === 'PRIME' ? 'bg-[#F84464]' : 'bg-indigo-400'"></span>
                  <span>{{ group.category }} — ₹{{ group.price.toFixed(2) }}</span>
                </span>
                <span class="text-[11px] text-slate-500 normal-case">Inclusive of GST</span>
              </div>

              <!-- Seat Rows under Category -->
              <div 
                v-for="row in group.rows" 
                :key="row.row" 
                class="flex items-center justify-center gap-2 sm:gap-3 py-0.5"
              >
                <!-- Left Row Letter -->
                <span class="w-5 text-xs font-bold text-slate-500 text-center select-none">{{ row.row }}</span>

                <!-- Left Wing Seats (e.g. 1 to 4) -->
                <div class="flex items-center gap-1.5 sm:gap-2">
                  <button
                    v-for="seat in getLeftBlock(row.seats)"
                    :key="seat.id"
                    :disabled="seat.status === 'BOOKED' || (seat.status === 'HELD' && !seat.held_by_me)"
                    @click="toggleSeatSelection(seat)"
                    class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg font-bold text-xs flex items-center justify-center transition-all duration-150 transform cursor-pointer"
                    :class="getSeatClasses(seat)"
                    :title="getSeatTooltip(seat)"
                  >
                    <span v-if="seat.status === 'BOOKED'" class="text-slate-600 text-[10px]">✕</span>
                    <span v-else>{{ seat.number }}</span>
                  </button>
                </div>

                <!-- Center Aisle Gap 1 -->
                <div class="w-3 sm:w-6 flex items-center justify-center">
                  <div class="w-0.5 h-6 bg-slate-800/40 rounded"></div>
                </div>

                <!-- Middle Main Block Seats (e.g. 5 to 14) -->
                <div class="flex items-center gap-1.5 sm:gap-2">
                  <button
                    v-for="seat in getCenterBlock(row.seats)"
                    :key="seat.id"
                    :disabled="seat.status === 'BOOKED' || (seat.status === 'HELD' && !seat.held_by_me)"
                    @click="toggleSeatSelection(seat)"
                    class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg font-bold text-xs flex items-center justify-center transition-all duration-150 transform cursor-pointer"
                    :class="getSeatClasses(seat)"
                    :title="getSeatTooltip(seat)"
                  >
                    <span v-if="seat.status === 'BOOKED'" class="text-slate-600 text-[10px]">✕</span>
                    <span v-else>{{ seat.number }}</span>
                  </button>
                </div>

                <!-- Center Aisle Gap 2 -->
                <div class="w-3 sm:w-6 flex items-center justify-center">
                  <div class="w-0.5 h-6 bg-slate-800/40 rounded"></div>
                </div>

                <!-- Right Wing Seats (e.g. 15 to 18) -->
                <div class="flex items-center gap-1.5 sm:gap-2">
                  <button
                    v-for="seat in getRightBlock(row.seats)"
                    :key="seat.id"
                    :disabled="seat.status === 'BOOKED' || (seat.status === 'HELD' && !seat.held_by_me)"
                    @click="toggleSeatSelection(seat)"
                    class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg font-bold text-xs flex items-center justify-center transition-all duration-150 transform cursor-pointer"
                    :class="getSeatClasses(seat)"
                    :title="getSeatTooltip(seat)"
                  >
                    <span v-if="seat.status === 'BOOKED'" class="text-slate-600 text-[10px]">✕</span>
                    <span v-else>{{ seat.number }}</span>
                  </button>
                </div>

                <!-- Right Row Letter -->
                <span class="w-5 text-xs font-bold text-slate-500 text-center select-none">{{ row.row }}</span>
              </div>
            </div>
          </div>

          <!-- BookMyShow Cinema Curved Screen (Bottom) -->
          <div class="w-full max-w-lg mx-auto text-center pt-8 pb-4">
            <svg viewBox="0 0 500 45" class="w-full h-9 filter drop-shadow-[0_0_12px_rgba(248,68,100,0.4)]">
              <path d="M 10 35 Q 250 5 490 35" fill="none" stroke="url(#screenGradBMS)" stroke-width="5" stroke-linecap="round" />
              <defs>
                <linearGradient id="screenGradBMS" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#334155" />
                  <stop offset="30%" stop-color="#F84464" />
                  <stop offset="50%" stop-color="#ffffff" />
                  <stop offset="70%" stop-color="#F84464" />
                  <stop offset="100%" stop-color="#334155" />
                </linearGradient>
              </defs>
            </svg>
            <span class="text-[10px] font-black tracking-[0.3em] uppercase text-slate-400 block mt-2">
              All eyes this way please
            </span>
          </div>

        </div>

        <!-- Modal Bottom Bar (BookMyShow Sticky Checkout Bar) -->
        <div class="p-4 sm:p-5 border-t border-slate-800 bg-[#1e202d] flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <div class="text-xs text-slate-400 flex items-center gap-1.5">
              <span>Selected Seats ({{ selectedSeatIds.length }}/{{ selectedQuantity }}):</span>
              <strong class="text-emerald-400 font-bold font-mono">{{ selectedSeatNames.join(', ') || 'Select on layout' }}</strong>
            </div>
            <div class="text-lg font-black text-white mt-0.5">
              Total Amount: <span class="text-white">₹{{ calculatedTotalBase.toFixed(2) }}</span>
              <span class="text-xs text-slate-400 font-normal ml-1">(+ 10% fee & GST at payment)</span>
            </div>
          </div>

          <button
            :disabled="selectedSeatIds.length === 0 || lockingInProgress"
            @click="proceedToCheckout"
            class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-black text-sm shadow-xl shadow-[#F84464]/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2 cursor-pointer"
          >
            <span v-if="lockingInProgress" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <CreditCard class="w-4 h-4" />
            <span>Pay ₹{{ calculatedTotalBase.toFixed(2) }}</span>
          </button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { X, Clock, AlertTriangle, CreditCard, ChevronRight, Edit2 } from 'lucide-vue-next'
import { api } from '../services/api'

const props = defineProps({
  show: { type: Object, required: true },
  userId: { type: String, required: true }
})

const emit = defineEmits(['close', 'proceed-checkout'])

// Flow: 'quantity' -> 'map'
const step = ref('quantity')
const selectedQuantity = ref(2)

const seatQuantities = [
  { count: 1, label: 'Cycle', icon: '🚲' },
  { count: 2, label: 'Scooter', icon: '🛵' },
  { count: 3, label: 'Auto', icon: '🛺' },
  { count: 4, label: 'Mini', icon: '🚗' },
  { count: 5, label: 'Sedan', icon: '🚘' },
  { count: 6, label: 'SUV', icon: '🚙' },
  { count: 8, label: 'Van', icon: '🚐' },
  { count: 10, label: 'Bus', icon: '🚍' },
]

const activeVehicle = computed(() => {
  return seatQuantities.find(q => q.count === selectedQuantity.value) || seatQuantities[1]
})

const loadingMatrix = ref(true)
const matrix = ref(null)
const selectedSeatIds = ref([])
const selectedSeatNames = ref([])
const lockingInProgress = ref(false)
const collisionError = ref('')

// 10-Minute Hold Countdown Timer (600s)
const timerSeconds = ref(600)
let timerInterval = null
let pollInterval = null

const formattedTimer = computed(() => {
  const m = Math.floor(timerSeconds.value / 60)
  const s = timerSeconds.value % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

// Group Rows by Category (Recliner, Prime, Classic)
const categorizedRows = computed(() => {
  if (!matrix.value?.rows) return []
  const groups = {}
  for (const r of matrix.value.rows) {
    const type = r.seat_type || 'CLASSIC'
    if (!groups[type]) {
      groups[type] = {
        category: type,
        price: r.seats[0]?.final_price || 200,
        rows: []
      }
    }
    groups[type].rows.push(r)
  }
  return Object.values(groups)
})

// BMS Aisle Layout Splitters (1-4, 5-14, 15-18)
function getLeftBlock(seats) {
  return seats.filter(s => s.number <= 4)
}

function getCenterBlock(seats) {
  return seats.filter(s => s.number > 4 && s.number <= 14)
}

function getRightBlock(seats) {
  return seats.filter(s => s.number > 14)
}

async function fetchMatrix() {
  try {
    const res = await api.getShowSeats(props.show.id, props.userId)
    matrix.value = res
  } catch (e) {
    console.error('Failed to fetch seat matrix:', e)
  } finally {
    loadingMatrix.value = false
  }
}

function startTimer() {
  if (timerInterval) clearInterval(timerInterval)
  timerSeconds.value = 600
  timerInterval = setInterval(() => {
    if (timerSeconds.value > 0) {
      timerSeconds.value--
    } else {
      clearInterval(timerInterval)
      collisionError.value = 'Seat hold timer expired! Your seat locks have been released.'
      selectedSeatIds.value = []
      selectedSeatNames.value = []
      fetchMatrix()
    }
  }, 1000)
}

function toggleSeatSelection(seat) {
  if (seat.status === 'BOOKED' || (seat.status === 'HELD' && !seat.held_by_me)) return

  const seatName = `${seat.row}${seat.number}`
  const idx = selectedSeatIds.value.indexOf(seat.id)

  if (idx >= 0) {
    selectedSeatIds.value.splice(idx, 1)
    const nIdx = selectedSeatNames.value.indexOf(seatName)
    if (nIdx >= 0) selectedSeatNames.value.splice(nIdx, 1)
  } else {
    // If selected seats reached desired quantity, shift selection or append up to limit
    if (selectedSeatIds.value.length >= selectedQuantity.value) {
      // Remove first seat and append new one for seamless group picking
      selectedSeatIds.value.shift()
      selectedSeatNames.value.shift()
    }
    selectedSeatIds.value.push(seat.id)
    selectedSeatNames.value.push(seatName)
  }

  if (selectedSeatIds.value.length === 1 && !timerInterval) {
    startTimer()
  }
}

function getSeatClasses(seat) {
  const isSelected = selectedSeatIds.value.includes(seat.id)
  if (isSelected) {
    return 'bg-[#1EA83C] text-white border-2 border-[#16A34A] shadow-md shadow-emerald-500/30 scale-105 font-black'
  }
  if (seat.status === 'BOOKED') {
    return 'bg-slate-900/90 text-slate-700 border border-slate-800/80 cursor-not-allowed'
  }
  if (seat.status === 'HELD') {
    if (seat.held_by_me) {
      return 'bg-amber-500 text-slate-950 font-black border border-amber-300 animate-pulse'
    }
    return 'bg-amber-500/20 border border-amber-500/40 text-amber-400 cursor-not-allowed'
  }
  return 'bg-[#222434] text-slate-300 border border-slate-700 hover:border-[#1EA83C] hover:text-[#1EA83C] hover:scale-110'
}

function getSeatTooltip(seat) {
  if (seat.status === 'BOOKED') return `Seat ${seat.row}${seat.number} is Booked`
  if (seat.status === 'HELD') return seat.held_by_me ? 'Held by you' : 'Held by another user'
  return `Seat ${seat.row}${seat.number} • ₹${seat.final_price}`
}

const calculatedTotalBase = computed(() => {
  if (!matrix.value) return 0.0
  let total = 0.0
  for (const r of matrix.value.rows) {
    for (const s of r.seats) {
      if (selectedSeatIds.value.includes(s.id)) {
        total += s.final_price
      }
    }
  }
  return total
})

async function proceedToCheckout() {
  if (selectedSeatIds.value.length === 0) return
  lockingInProgress.value = true
  collisionError.value = ''

  try {
    const res = await api.lockSeats(props.show.id, selectedSeatIds.value, props.userId)
    if (res.success) {
      emit('proceed-checkout', {
        showId: props.show.id,
        seatIds: selectedSeatIds.value,
        seatNames: selectedSeatNames.value,
        totalBase: calculatedTotalBase.value
      })
    }
  } catch (err) {
    if (err.status === 423) {
      collisionError.value = 'HTTP 423 Locked: One or more selected seats were locked by another user! Matrix refreshed.'
    } else {
      collisionError.value = err.message || 'Failed to acquire seat lock.'
    }
    fetchMatrix()
  } finally {
    lockingInProgress.value = false
  }
}

onMounted(() => {
  fetchMatrix()
  pollInterval = setInterval(fetchMatrix, 5000)
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
  if (pollInterval) clearInterval(pollInterval)
})
</script>
