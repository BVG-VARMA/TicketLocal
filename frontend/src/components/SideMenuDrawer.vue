<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-hidden select-none">
    <!-- Backdrop -->
    <div 
      class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity animate-in fade-in duration-200"
      @click="$emit('close')"
    ></div>

    <!-- Slide-in Drawer -->
    <div class="fixed inset-y-0 right-0 max-w-sm w-full bg-[#181a24] border-l border-slate-700 shadow-2xl flex flex-col justify-between animate-in slide-in-from-right duration-300 z-10">
      
      <!-- Drawer Top / User Banner -->
      <div>
        <div class="p-6 bg-[#202230] border-b border-slate-800 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-2xl bg-[#F84464] text-white font-black text-xl flex items-center justify-center shadow-lg shadow-[#F84464]/30">
              {{ (userName || 'C')[0].toUpperCase() }}
            </div>
            <div>
              <div class="flex items-center gap-1.5">
                <h3 class="font-black text-base text-white">Hey, {{ userName }}!</h3>
                <span class="px-1.5 py-0.2 rounded bg-emerald-950 border border-emerald-700 text-[9px] font-bold text-emerald-400">Citizen</span>
              </div>
              <button 
                @click="$emit('open-auth'); $emit('close')"
                class="text-xs text-[#F84464] font-bold hover:underline cursor-pointer flex items-center gap-1 mt-0.5"
              >
                <span>{{ isLoggedIn ? 'Citizen Pass & Profile' : 'Citizen Sign In / Register' }}</span>
                <span>→</span>
              </button>
            </div>
          </div>
          <button 
            @click="$emit('close')"
            class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors cursor-pointer"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Menu Navigation Items -->
        <div class="p-4 space-y-1 overflow-y-auto max-h-[calc(100vh-210px)] text-sm">
          
          <!-- Admin Portal Entry -->
          <button 
            @click="$emit('open-admin'); $emit('close')"
            class="w-full flex items-center justify-between p-3 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-bold transition-colors cursor-pointer"
          >
            <div class="flex items-center gap-3">
              <ShieldCheck class="w-5 h-5 text-amber-400" />
              <span class="text-xs">Admin Cinema Manager</span>
            </div>
            <span class="px-1.5 py-0.5 rounded bg-amber-500 text-slate-950 text-[9px] font-black">ADMIN</span>
          </button>

          <button 
            @click="$emit('open-bookings'); $emit('close')"
            class="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
          >
            <div class="flex items-center gap-3">
              <Ticket class="w-5 h-5 text-[#F84464]" />
              <span class="font-semibold text-xs">Citizen Bookings & M-Tickets</span>
            </div>
            <span 
              v-if="bookingCount > 0"
              class="px-2 py-0.5 rounded-full bg-[#F84464] text-white font-bold text-[10px]"
            >
              {{ bookingCount }}
            </span>
          </button>

          <button 
            @click="$emit('open-category', 'Stream'); $emit('close')"
            class="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
          >
            <div class="flex items-center gap-3">
              <Tv class="w-5 h-5 text-amber-400" />
              <span class="font-semibold text-xs">CinePass Stream & Premieres</span>
            </div>
            <span class="px-1.5 py-0.5 rounded bg-[#F84464] text-white text-[9px] font-bold">NEW</span>
          </button>

          <button 
            @click="$emit('open-category', 'Offers'); $emit('close')"
            class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
          >
            <Percent class="w-5 h-5 text-emerald-400" />
            <span class="font-semibold text-xs">Offers & Discounts</span>
          </button>

          <button 
            @click="$emit('open-category', 'Gift Cards'); $emit('close')"
            class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
          >
            <Gift class="w-5 h-5 text-purple-400" />
            <span class="font-semibold text-xs">CinePass Gift Cards</span>
          </button>

          <button 
            @click="$emit('open-category', 'ListYourShow'); $emit('close')"
            class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
          >
            <Clapperboard class="w-5 h-5 text-cyan-400" />
            <span class="font-semibold text-xs">List Your Show</span>
          </button>

          <button 
            @click="$emit('open-category', 'Corporates'); $emit('close')"
            class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
          >
            <Building class="w-5 h-5 text-yellow-400" />
            <span class="font-semibold text-xs">Corporates & Bulk Tickets</span>
          </button>

          <div class="border-t border-slate-800 my-2 pt-2">
            <button 
              @click="$emit('open-category', 'Buzz'); $emit('close')"
              class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-800 text-slate-200 hover:text-white transition-colors cursor-pointer"
            >
              <HelpCircle class="w-5 h-5 text-slate-400" />
              <span class="font-semibold text-xs">Buzz & Cinema News</span>
            </button>
          </div>

        </div>
      </div>

      <!-- Drawer Bottom Actions -->
      <div class="p-6 border-t border-slate-800 bg-[#202230]/60 space-y-3">
        <button 
          v-if="!isLoggedIn"
          @click="$emit('open-auth'); $emit('close')"
          class="w-full py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 transition-all cursor-pointer text-center"
        >
          Citizen Sign-In to CinePass
        </button>

        <button 
          v-else
          @click="$emit('logout'); $emit('close')"
          class="w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-rose-400 font-bold text-xs border border-slate-700 transition-all cursor-pointer flex items-center justify-center gap-2"
        >
          <LogOut class="w-4 h-4" />
          <span>Sign Out Citizen Session</span>
        </button>

        <div class="text-[10px] text-slate-500 text-center">
          CinePass Entertainment App • Verified Citizen Portal
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { X, Ticket, Tv, Percent, Gift, Clapperboard, Building, HelpCircle, LogOut, ShieldCheck } from 'lucide-vue-next'

defineProps({
  isOpen: { type: Boolean, default: false },
  userName: { type: String, default: 'Citizen' },
  isLoggedIn: { type: Boolean, default: false },
  bookingCount: { type: Number, default: 0 }
})

defineEmits(['close', 'open-auth', 'open-admin', 'open-bookings', 'open-category', 'logout'])
</script>
