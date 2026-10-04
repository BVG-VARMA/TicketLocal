<template>
  <div class="min-h-screen pb-20 pt-8 px-4 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Back Link & Title -->
      <div class="flex items-center justify-between mb-6">
        <router-link
          :to="`/shows/${showId}/seats`"
          class="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          ← Change Seats
        </router-link>

        <!-- Timer badge -->
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold animate-pulse">
          <span>⏳</span>
          <span>Time Remaining: {{ bookingStore.formattedTimer }}</span>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left: Payment Form & Test Card Helpers -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bms-card rounded-2xl p-6 border border-white/10 shadow-2xl">
            <h2 class="text-lg font-bold text-white mb-2 flex items-center gap-2">
              <span>💳</span>
              <span>Payment Simulator</span>
            </h2>
            <p class="text-xs text-slate-400 mb-6">
              All transactions are simulated locally with full ACID guarantees in PostgreSQL.
            </p>

            <!-- Test Card Fill Shortcuts -->
            <div class="p-3.5 rounded-xl bg-white/5 border border-white/10 mb-6 flex flex-wrap items-center justify-between gap-3">
              <span class="text-xs font-semibold text-slate-300">Quick Test Cards:</span>
              <div class="flex items-center gap-2">
                <button
                  @click="fillValidCard"
                  class="px-3 py-1 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-300 text-xs font-bold transition-all"
                >
                  ✓ Valid Card
                </button>
                <button
                  @click="fillDeclinedCard"
                  class="px-3 py-1 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-300 text-xs font-bold transition-all"
                >
                  ✕ Decline Card
                </button>
              </div>
            </div>

            <!-- Card Details Form -->
            <form @submit.prevent="handlePay" class="space-y-4">
              <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Card Number
                </label>
                <input
                  v-model="card.cardNumber"
                  type="text"
                  required
                  placeholder="4000 1234 5678 9010"
                  class="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white font-mono placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Cardholder Name
                </label>
                <input
                  v-model="card.cardHolder"
                  type="text"
                  required
                  placeholder="John Citizen"
                  class="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
                />
              </div>

              <div class="grid grid-cols-3 gap-3">
                <div>
                  <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Expiry MM
                  </label>
                  <input
                    v-model="card.expiryMonth"
                    type="text"
                    maxlength="2"
                    required
                    placeholder="12"
                    class="w-full px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white font-mono text-center placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
                  />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Expiry YY
                  </label>
                  <input
                    v-model="card.expiryYear"
                    type="text"
                    maxlength="4"
                    required
                    placeholder="28"
                    class="w-full px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white font-mono text-center placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
                  />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    CVV
                  </label>
                  <input
                    v-model="card.cvv"
                    type="password"
                    maxlength="4"
                    required
                    placeholder="•••"
                    class="w-full px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white font-mono text-center placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
                  />
                </div>
              </div>

              <!-- Payment Button with 2s Loading State -->
              <button
                type="submit"
                :disabled="bookingStore.loadingCheckout"
                class="w-full mt-6 py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white text-sm font-extrabold transition-all shadow-lg shadow-[#F84464]/30 hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:pointer-events-none flex items-center justify-center gap-2"
              >
                <span v-if="bookingStore.loadingCheckout" class="inline-flex items-center gap-2">
                  <span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  Processing Payment & Minting QR Ticket...
                </span>
                <span v-else>
                  Pay ₹{{ quote?.total?.toFixed(2) || '0.00' }} & Confirm
                </span>
              </button>
            </form>
          </div>
        </div>

        <!-- Right: Order Summary & Itemized Breakdown -->
        <div class="space-y-6">
          <div class="bms-card rounded-2xl p-6 border border-white/10 shadow-2xl">
            <h3 class="text-base font-bold text-white pb-3 border-b border-white/10 mb-4">
              Booking Summary
            </h3>

            <!-- Show Info -->
            <div class="mb-4">
              <div class="text-sm font-bold text-white">{{ bookingStore.seatMatrix?.content_title }}</div>
              <div class="text-xs text-slate-400 mt-0.5">
                {{ bookingStore.seatMatrix?.theater_name }} • {{ bookingStore.seatMatrix?.screen_name }}
              </div>
            </div>

            <!-- Seats list -->
            <div class="py-3 border-y border-white/10 mb-4">
              <div class="text-xs text-slate-400 font-semibold mb-2">Reserved Seats:</div>
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="s in bookingStore.selectedSeats"
                  :key="s.id"
                  class="px-2.5 py-1 rounded-md bg-white/10 text-white text-xs font-mono font-bold"
                >
                  {{ s.row_label }}{{ s.seat_number }} (₹{{ s.computed_price }})
                </span>
              </div>
            </div>

            <!-- Itemized Pricing Breakdown -->
            <div class="space-y-2.5 text-xs text-slate-300">
              <div class="flex justify-between">
                <span>Seats Subtotal</span>
                <span class="font-mono font-bold text-white">₹{{ quote?.subtotal?.toFixed(2) || '0.00' }}</span>
              </div>
              <div class="flex justify-between">
                <span>Convenience Fee (10%)</span>
                <span class="font-mono font-bold text-white">₹{{ quote?.convenience_fee?.toFixed(2) || '0.00' }}</span>
              </div>
              <div class="flex justify-between">
                <span>Integrated GST Tax (18%)</span>
                <span class="font-mono font-bold text-white">₹{{ quote?.tax?.toFixed(2) || '0.00' }}</span>
              </div>
              <div class="pt-3 border-t border-white/10 flex justify-between text-sm font-extrabold text-white">
                <span>Grand Total</span>
                <span class="font-mono text-[#F84464] text-base">₹{{ quote?.total?.toFixed(2) || '0.00' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookingStore } from '../stores/booking'
import { useToastStore } from '../stores/toast'

const route = useRoute()
const router = useRouter()
const bookingStore = useBookingStore()
const toastStore = useToastStore()

const showId = parseInt(route.params.showId)
const quote = ref(null)

const card = reactive({
  cardNumber: '4000 1234 5678 9010',
  cardHolder: 'Demo Citizen',
  expiryMonth: '12',
  expiryYear: '28',
  cvv: '123',
})

function fillValidCard() {
  card.cardNumber = '4000 1234 5678 9010'
  card.cardHolder = 'Demo Citizen'
  card.expiryMonth = '12'
  card.expiryYear = '28'
  card.cvv = '123'
}

function fillDeclinedCard() {
  card.cardNumber = '4000 0000 0000 0002'
  card.cardHolder = 'Decline Citizen'
  card.expiryMonth = '11'
  card.expiryYear = '29'
  card.cvv = '999'
}

async function handlePay() {
  const paymentPayload = {
    card_number: card.cardNumber.replace(/\s+/g, ''),
    card_holder: card.cardHolder,
    expiry_month: card.expiryMonth,
    expiry_year: card.expiryYear,
    cvv: card.cvv,
  }

  const res = await bookingStore.checkout(showId, paymentPayload)
  if (res.success) {
    router.push(`/confirmation/${res.data.booking_id}`)
  }
}

onMounted(async () => {
  if (bookingStore.selectedSeats.length === 0) {
    router.push(`/shows/${showId}/seats`)
    return
  }

  try {
    quote.value = await bookingStore.fetchCartQuote(showId)
  } catch (e) {
    console.error(e)
  }
})
</script>
