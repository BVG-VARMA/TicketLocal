<template>
  <div v-if="checkoutData" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/90 backdrop-blur-md animate-in fade-in duration-200">
    <div class="bg-[#1a1c26] w-full max-w-lg rounded-3xl border border-slate-700 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200 my-auto select-none">
      
      <!-- Modal Header (BMS Order Summary) -->
      <div class="p-5 border-b border-slate-800 bg-[#222434] flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-[#F84464]/20 border border-[#F84464]/40 flex items-center justify-center">
            <ShieldCheck class="w-5 h-5 text-[#F84464]" />
          </div>
          <div>
            <h2 class="text-base font-black text-white">Order Summary</h2>
            <p class="text-[10px] text-slate-400">CinePass Secure Payment Gateway</p>
          </div>
        </div>
        <button 
          :disabled="isProcessing"
          @click="$emit('close')"
          class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors disabled:opacity-30 cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Processing State Overlay -->
      <div v-if="isProcessing" class="p-12 text-center space-y-4">
        <div class="w-14 h-14 border-4 border-[#F84464] border-t-transparent rounded-full animate-spin mx-auto"></div>
        <h3 class="text-lg font-black text-white">Authorizing Payment...</h3>
        <p class="text-xs text-slate-400 max-w-xs mx-auto leading-relaxed">
          Simulating instant payment settlement & issuing your official CinePass M-Ticket. Please do not refresh.
        </p>
      </div>

      <!-- Checkout Form -->
      <div v-else class="p-5 sm:p-6 space-y-5">
        
        <!-- Error Alert -->
        <div v-if="errorMessage" class="p-3.5 rounded-2xl bg-rose-950/90 border border-rose-500 text-rose-200 text-xs flex items-center gap-2">
          <AlertCircle class="w-4 h-4 text-rose-400 shrink-0" />
          <span>{{ errorMessage }}</span>
        </div>

        <!-- Order Summary Card -->
        <div class="bg-[#222434]/80 p-4 rounded-2xl border border-slate-800 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-800/80 pb-2">
            <div>
              <span class="text-xs text-slate-400 font-medium block">Selected Cinema Seats</span>
              <span class="text-sm font-black text-white">{{ checkoutData.seatNames.join(', ') }}</span>
            </div>
            <span class="px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-800 text-emerald-400 text-[10px] font-bold uppercase">
              Locked
            </span>
          </div>

          <!-- Price Breakdown -->
          <div v-if="feeBreakdown" class="space-y-2 text-xs">
            <div class="flex justify-between text-slate-300">
              <span>Ticket Subtotal ({{ feeBreakdown.seat_count }} seats)</span>
              <span>₹{{ feeBreakdown.base_amount.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-slate-300">
              <span>CinePass Convenience Fee (10%)</span>
              <span>₹{{ feeBreakdown.convenience_fee.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-slate-300">
              <span>Integrated GST @ 18%</span>
              <span>₹{{ feeBreakdown.tax_amount.toFixed(2) }}</span>
            </div>

            <!-- F&B Snacks Item if selected -->
            <div v-if="selectedSnack" class="flex justify-between text-amber-400 font-medium pt-1 border-t border-slate-800/60">
              <span>🍿 {{ selectedSnack.name }}</span>
              <span>₹{{ selectedSnack.price.toFixed(2) }}</span>
            </div>

            <div class="pt-2 border-t border-slate-800 flex justify-between text-base font-black text-white">
              <span>Total Payable Amount</span>
              <span class="text-[#F84464] text-lg">₹{{ totalWithSnacks.toFixed(2) }}</span>
            </div>
          </div>
          <div v-else class="py-4 text-center text-xs text-slate-400">
            Calculating BookMyShow fee breakdown...
          </div>
        </div>

        <!-- Grab a Bite! (BookMyShow F&B Add-ons) -->
        <div class="bg-[#222434]/50 p-3.5 rounded-2xl border border-slate-800 space-y-2.5">
          <div class="flex items-center justify-between">
            <h4 class="text-xs font-bold text-white flex items-center gap-1.5">
              <span>🍿 Grab a Bite at Cinema!</span>
            </h4>
            <span class="text-[10px] text-slate-400">Optional Add-on</span>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="snack in snackOptions"
              :key="snack.id"
              @click="toggleSnack(snack)"
              class="p-2 rounded-xl border text-center transition-all flex flex-col items-center justify-center select-none cursor-pointer"
              :class="selectedSnack?.id === snack.id ? 'bg-[#F84464]/20 border-[#F84464] text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'"
            >
              <span class="text-base">{{ snack.icon }}</span>
              <span class="text-[10px] font-bold line-clamp-1 mt-0.5">{{ snack.name }}</span>
              <span class="text-[10px] font-semibold text-emerald-400">₹{{ snack.price }}</span>
            </button>
          </div>
        </div>

        <!-- Contact Information (Auto-populated with User Profile) -->
        <div class="space-y-2.5">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Contact & M-Ticket Details</h3>
            <span class="text-[10px] text-slate-500">M-Ticket will be delivered here</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div>
              <label class="text-[10px] text-slate-400 block mb-1">Your Full Name</label>
              <input 
                v-model="customerName"
                type="text" 
                placeholder="Rahul Sharma"
                class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
              />
            </div>
            <div>
              <label class="text-[10px] text-slate-400 block mb-1">Email for M-Ticket</label>
              <input 
                v-model="customerEmail"
                type="email" 
                placeholder="rahul@example.com"
                class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
              />
            </div>
          </div>
        </div>

        <!-- Payment Mode Selector (BMS Options) -->
        <div class="space-y-2.5">
          <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Select Payment Mode</h3>
          <div class="grid grid-cols-3 gap-2.5">
            <button
              v-for="pm in paymentMethods"
              :key="pm.id"
              @click="selectedMethod = pm.id"
              class="p-2.5 rounded-xl border text-center transition-all flex flex-col items-center justify-center gap-1 select-none cursor-pointer"
              :class="selectedMethod === pm.id ? 'bg-[#F84464]/20 border-[#F84464] text-white shadow-md' : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'"
            >
              <component :is="pm.icon" class="w-4 h-4 text-[#F84464]" />
              <span class="text-[10px] font-bold">{{ pm.name }}</span>
            </button>
          </div>
        </div>

        <!-- Pay Button -->
        <button
          :disabled="!feeBreakdown || !customerName || !customerEmail || isProcessing"
          @click="submitPayment"
          class="w-full py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-black text-sm shadow-xl shadow-[#F84464]/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2 cursor-pointer"
        >
          <Lock class="w-4 h-4" />
          <span>Pay ₹{{ totalWithSnacks.toFixed(2) }}</span>
        </button>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { X, ShieldCheck, AlertCircle, Lock, QrCode, CreditCard, Building2 } from 'lucide-vue-next'
import { api } from '../services/api'

const props = defineProps({
  checkoutData: { type: Object, required: true },
  userId: { type: String, required: true },
  currentUser: { type: Object, default: () => ({ guest_name: 'Rahul Sharma', guest_email: 'user@bookmyshow.com', guest_phone: '+91 98765 43210' }) }
})

const emit = defineEmits(['close', 'payment-success'])

const feeBreakdown = ref(null)
const isProcessing = ref(false)
const errorMessage = ref('')

const customerName = ref(props.currentUser?.guest_name || 'Rahul Sharma')
const customerEmail = ref(props.currentUser?.guest_email || 'user@bookmyshow.com')
const customerPhone = ref(props.currentUser?.guest_phone || '+91 98765 43210')
const selectedMethod = ref('MOCK_UPI')
const selectedSnack = ref(null)

watch(() => props.currentUser, (newVal) => {
  if (newVal) {
    customerName.value = newVal.guest_name || 'Rahul Sharma'
    customerEmail.value = newVal.guest_email || 'user@bookmyshow.com'
    customerPhone.value = newVal.guest_phone || '+91 98765 43210'
  }
}, { immediate: true })

const snackOptions = [
  { id: 'popcorn', name: 'Caramel Popcorn', price: 180, icon: '🍿' },
  { id: 'combo', name: 'Pepsi + Popcorn', price: 240, icon: '🥤' },
  { id: 'nachos', name: 'Cheesy Nachos', price: 190, icon: '🧀' },
]

const paymentMethods = [
  { id: 'MOCK_UPI', name: 'UPI / GPay', icon: QrCode },
  { id: 'MOCK_CARD', name: 'Credit/Debit Card', icon: CreditCard },
  { id: 'MOCK_NETBANKING', name: 'NetBanking', icon: Building2 },
]

const totalWithSnacks = computed(() => {
  if (!feeBreakdown.value) return 0.0
  const snackPrice = selectedSnack.value ? selectedSnack.value.price : 0
  return feeBreakdown.value.total_amount + snackPrice
})

const toggleSnack = (snack) => {
  if (selectedSnack.value?.id === snack.id) {
    selectedSnack.value = null
  } else {
    selectedSnack.value = snack
  }
}

async function loadFees() {
  try {
    feeBreakdown.value = await api.calculateFees(props.checkoutData.showId, props.checkoutData.seatIds)
  } catch (err) {
    errorMessage.value = err.message || 'Failed to calculate fee breakdown.'
  }
}

async function submitPayment() {
  if (!customerName.value || !customerEmail.value) {
    errorMessage.value = 'Please provide contact name and email.'
    return
  }

  isProcessing.value = true
  errorMessage.value = ''

  try {
    const response = await api.processCheckout({
      show_id: props.checkoutData.showId,
      seat_ids: props.checkoutData.seatIds,
      user_id: props.userId,
      customer_name: customerName.value,
      customer_email: customerEmail.value,
      customer_phone: customerPhone.value || '+91 98765 43210',
      payment_method: selectedMethod.value
    })

    emit('payment-success', response)
  } catch (err) {
    errorMessage.value = err.message || 'Payment processing failed.'
    isProcessing.value = false
  } finally {
    isProcessing.value = false
  }
}

onMounted(() => {
  loadFees()
})
</script>
