<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/90 backdrop-blur-md">
    <div class="bg-[#1a1c26] w-full max-w-2xl rounded-3xl border border-slate-700 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200 flex flex-col max-h-[85vh] my-auto">
      
      <!-- Drawer Header (BMS Purchase History) -->
      <div class="p-5 border-b border-slate-800 bg-[#222434] flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-[#F84464]/20 border border-[#F84464]/40 flex items-center justify-center">
            <Ticket class="w-5 h-5 text-[#F84464]" />
          </div>
          <div>
            <h2 class="text-base font-black text-white">Purchase History & M-Tickets</h2>
            <p class="text-[10px] text-slate-400">CinePass Active & Past Bookings</p>
          </div>
        </div>
        <button 
          @click="$emit('close')"
          class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Bookings List Body -->
      <div class="p-5 sm:p-6 overflow-y-auto flex-1 space-y-4">
        <div v-if="bookings.length === 0" class="py-16 text-center text-slate-500">
          <Ticket class="w-12 h-12 stroke-[1.5] text-slate-600 mx-auto mb-3" />
          <h3 class="text-base font-bold text-slate-300">No CinePass Bookings Yet</h3>
          <p class="text-xs text-slate-500 mt-1">Book your tickets for movies & cinema shows to view your digital M-Tickets here.</p>
        </div>

        <div 
          v-for="b in bookings" 
          :key="b.booking_ref"
          class="bg-[#222434] p-4 rounded-2xl border border-slate-800 hover:border-slate-700 transition-all flex flex-col sm:flex-row items-center justify-between gap-4"
        >
          <div class="flex items-center gap-4 w-full sm:w-auto">
            <div class="w-14 h-14 rounded-xl bg-white p-1 flex items-center justify-center shrink-0 border border-slate-300 shadow">
              <img 
                v-if="b.ticket_qr_url" 
                :src="b.ticket_qr_url" 
                alt="QR"
                class="w-full h-full object-contain"
              />
              <QrCode v-else class="w-8 h-8 text-[#F84464]" />
            </div>

            <div class="flex-1">
              <div class="flex items-center gap-2">
                <span class="text-xs font-mono font-bold text-[#F84464]">{{ b.booking_ref }}</span>
                <span class="px-2 py-0.2 rounded bg-emerald-950/60 border border-emerald-800 text-[10px] font-bold text-emerald-400 uppercase">
                  {{ b.status }}
                </span>
              </div>
              <h4 class="font-bold text-base text-white mt-0.5">{{ b.movie_title }}</h4>
              <p class="text-xs text-slate-300 mt-0.5">
                {{ b.theater_name }} • <strong class="text-amber-400">{{ b.seats ? b.seats.join(', ') : 'Seats' }}</strong>
              </p>
              <p class="text-[10px] text-slate-400 mt-0.5">Show: {{ b.show_date }} @ {{ b.show_time }}</p>
            </div>
          </div>

          <button
            @click="$emit('view-ticket', b)"
            class="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow transition-all flex items-center justify-center gap-2 shrink-0 select-none"
          >
            <Eye class="w-4 h-4" />
            <span>View M-Ticket</span>
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { X, Ticket, QrCode, Eye } from 'lucide-vue-next'

defineProps({
  isOpen: { type: Boolean, default: false },
  bookings: { type: Array, default: () => [] }
})

defineEmits(['close', 'view-ticket'])
</script>
