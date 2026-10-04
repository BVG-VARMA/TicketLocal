<template>
  <div v-if="ticket" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/90 backdrop-blur-md">
    <div class="bg-[#1a1c26] w-full max-w-lg rounded-3xl border border-slate-700 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-300 my-auto">
      
      <!-- BookMyShow M-Ticket Header -->
      <div class="p-5 border-b border-slate-800 bg-[#F84464] text-white flex items-center justify-between shadow-lg">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center">
            <CheckCircle2 class="w-6 h-6 text-white stroke-[2.5]" />
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <span class="text-xs font-black tracking-wider uppercase bg-white text-[#F84464] px-2 py-0.5 rounded-lg font-mono">
                CINEPASS M-TICKET
              </span>
            </div>
            <p class="text-xs font-bold text-white/90 mt-0.5 font-mono">Citizen Pass Ref: {{ ticket.booking_ref }}</p>
          </div>
        </div>

        <button 
          @click="$emit('close')"
          class="p-2 rounded-full bg-black/20 hover:bg-black/40 text-white transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Ticket Card Body -->
      <div id="printable-ticket" class="p-5 sm:p-6 space-y-5 bg-[#14151e]">
        
        <!-- Movie Details Card -->
        <div class="flex items-start gap-4 bg-[#222434] p-4 rounded-2xl border border-slate-800">
          <img 
            v-if="ticket.movie_poster"
            :src="ticket.movie_poster" 
            :alt="ticket.movie_title"
            class="w-20 rounded-xl border border-slate-700 shadow-lg shrink-0 aspect-[2/3] object-cover"
          />
          <div class="flex-1">
            <span class="px-2 py-0.5 rounded bg-[#F84464]/20 border border-[#F84464]/40 text-[10px] font-black text-[#F84464] uppercase">
              {{ ticket.format }}
            </span>
            <h3 class="text-lg sm:text-xl font-black text-white tracking-tight mt-1 line-clamp-1">
              {{ ticket.movie_title }}
            </h3>
            <p class="text-xs text-slate-300 mt-0.5">
              {{ ticket.language }} • <strong class="text-white">{{ ticket.theater_name }}</strong>
            </p>
            <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">
              {{ ticket.theater_address }}
            </p>
          </div>
        </div>

        <!-- Showtime & Seat Grid -->
        <div class="grid grid-cols-2 gap-3 text-xs">
          <div class="bg-[#222434] p-3.5 rounded-2xl border border-slate-800">
            <span class="text-slate-400 font-medium block">Show Date & Time</span>
            <span class="text-sm font-black text-white block mt-0.5">{{ ticket.show_date }}</span>
            <span class="text-xs font-bold text-[#F84464]">{{ ticket.show_time }}</span>
          </div>

          <div class="bg-[#222434] p-3.5 rounded-2xl border border-slate-800">
            <span class="text-slate-400 font-medium block">Auditorium & Seats</span>
            <span class="text-sm font-black text-white block mt-0.5">{{ ticket.screen_name }}</span>
            <span class="text-xs font-black text-emerald-400">{{ ticket.seats.join(', ') }}</span>
          </div>
        </div>

        <!-- Local PNG QR Code Scanner Card -->
        <div class="bg-[#222434] p-5 rounded-2xl border border-slate-800 text-center flex flex-col items-center justify-center space-y-3">
          <div class="p-3 rounded-2xl bg-white border border-slate-300 shadow-md inline-block">
            <img 
              :src="ticket.ticket_qr_url" 
              alt="BookMyShow QR Ticket Scanner"
              class="w-40 h-40 object-contain"
            />
          </div>
          <div>
            <span class="text-xs font-mono font-black text-white block tracking-widest uppercase">
              TURNSTILE ENTRY QR CODE
            </span>
            <span class="text-[10px] text-slate-400 block mt-0.5">
              Scan this QR code or show on your phone at cinema entrance
            </span>
          </div>
        </div>

        <!-- Payment Breakdown -->
        <div class="bg-[#222434]/80 p-4 rounded-2xl border border-slate-800 space-y-1.5 text-xs">
          <div class="flex justify-between text-slate-400">
            <span>Customer Name</span>
            <span class="text-white font-semibold">{{ ticket.customer_name }}</span>
          </div>
          <div class="flex justify-between text-slate-400">
            <span>Payment Reference</span>
            <span class="text-slate-300 font-mono">{{ ticket.payment_id }}</span>
          </div>
          <div class="flex justify-between text-slate-400">
            <span>Payment Status</span>
            <span class="text-emerald-400 font-bold uppercase">{{ ticket.status }}</span>
          </div>
          <div class="pt-2 border-t border-slate-800 flex justify-between text-sm font-black text-white">
            <span>Total Paid (incl. Taxes)</span>
            <span class="text-emerald-400">₹{{ ticket.total_amount.toFixed(2) }}</span>
          </div>
        </div>

      </div>

      <!-- Action Buttons (Save / Print) -->
      <div class="p-4 sm:p-5 border-t border-slate-800 bg-[#222434] flex items-center justify-between gap-3">
        <a
          :href="ticket.ticket_qr_url"
          download
          target="_blank"
          class="flex-1 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs flex items-center justify-center gap-2 transition-all border border-slate-700 select-none"
        >
          <Download class="w-4 h-4 text-[#F84464]" />
          <span>Save M-Ticket</span>
        </a>

        <button
          @click="printTicket"
          class="flex-1 py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-lg shadow-[#F84464]/30 select-none"
        >
          <Printer class="w-4 h-4" />
          <span>Print Ticket</span>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { X, CheckCircle2, Download, Printer } from 'lucide-vue-next'
import confetti from 'canvas-confetti'

const props = defineProps({
  ticket: { type: Object, required: true }
})

defineEmits(['close'])

function triggerCelebration() {
  try {
    confetti({
      particleCount: 90,
      spread: 75,
      origin: { y: 0.6 }
    })
  } catch (e) {
    // ignore
  }
}

function printTicket() {
  window.print()
}

onMounted(() => {
  triggerCelebration()
})
</script>
