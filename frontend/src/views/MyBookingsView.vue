<template>
  <div class="min-h-screen pb-20 pt-8 px-4 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <div class="flex items-center justify-between pb-4 border-b border-white/10 mb-8">
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
            My Bookings & Passes
          </h1>
          <p class="text-xs text-slate-400 mt-1">
            Access your active cinema tickets and download offline QR codes.
          </p>
        </div>
        <router-link
          to="/"
          class="px-4 py-2 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white text-xs font-bold transition-all shadow-md shadow-[#F84464]/20"
        >
          + Book New Show
        </router-link>
      </div>

      <div v-if="loading" class="space-y-4">
        <div v-for="n in 3" :key="n" class="h-44 rounded-2xl bg-white/5 animate-pulse"></div>
      </div>

      <div v-else-if="bookings.length > 0" class="space-y-6">
        <div
          v-for="b in bookings"
          :key="b.id"
          class="bms-card rounded-2xl p-6 border border-white/10 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6"
        >
          <!-- Left: Show Info -->
          <div class="flex-1 space-y-2">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold uppercase tracking-wider">
                ● {{ b.status }}
              </span>
              <span class="text-xs font-mono text-slate-400">#{{ b.id }}</span>
            </div>
            <h2 class="text-lg font-bold text-white">
              {{ b.content_title }}
            </h2>
            <div class="text-xs text-slate-300">
              🏛️ {{ b.theater_name }} • {{ b.screen_name }}
            </div>
            <div class="text-xs text-slate-400">
              📅 {{ formatDateTime(b.start_time) }}
            </div>
            <div class="pt-2 flex flex-wrap gap-1.5">
              <span
                v-for="s in b.seats"
                :key="s.seat_id"
                class="px-2 py-0.5 rounded bg-white/10 text-white text-xs font-mono font-semibold"
              >
                {{ s.row_label }}{{ s.seat_number }}
              </span>
            </div>
          </div>

          <!-- Middle: Price -->
          <div class="text-left md:text-right border-t md:border-t-0 md:border-l border-white/10 pt-4 md:pt-0 md:pl-6">
            <div class="text-xs text-slate-400">Total Paid</div>
            <div class="text-xl font-extrabold text-white font-mono">
              ₹{{ b.total.toFixed(2) }}
            </div>
          </div>

          <!-- Right: QR Code & Actions -->
          <div v-if="b.ticket" class="flex flex-col sm:flex-row items-center gap-3">
            <img
              :src="b.ticket.qr_url"
              alt="QR"
              class="w-20 h-20 rounded-xl bg-white p-1 border border-white/20 shadow-md"
            />
            <div class="flex flex-col gap-2 w-full sm:w-auto">
              <a
                :href="b.ticket.qr_url"
                download
                class="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold text-center transition-all border border-white/10"
              >
                📥 Download PNG
              </a>
              <router-link
                :to="`/confirmation/${b.id}`"
                class="px-3.5 py-2 rounded-xl bg-[#F84464]/20 hover:bg-[#F84464]/30 text-[#F84464] border border-[#F84464]/40 text-xs font-bold text-center transition-all"
              >
                View Pass
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20 bg-white/5 rounded-3xl border border-white/10">
        <div class="text-4xl mb-3">🎟️</div>
        <h3 class="text-lg font-bold text-white">No active bookings yet</h3>
        <p class="text-xs text-slate-400 mt-1 mb-6">
          Explore movies and book your first cinema pass.
        </p>
        <router-link
          to="/"
          class="px-6 py-2.5 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white text-xs font-bold shadow-lg shadow-[#F84464]/30 transition-all"
        >
          Explore Movies Now
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/client'

const bookings = ref([])
const loading = ref(true)

async function fetchBookings() {
  loading.value = true
  try {
    const resp = await apiClient.get('/bookings')
    bookings.value = resp.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
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
  fetchBookings()
})
</script>
