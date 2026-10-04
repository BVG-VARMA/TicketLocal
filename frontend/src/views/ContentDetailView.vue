<template>
  <div class="min-h-screen pb-20">
    <div v-if="loading" class="max-w-7xl mx-auto px-4 py-16">
      <div class="h-96 rounded-3xl bg-white/5 animate-pulse"></div>
    </div>

    <div v-else-if="content">
      <!-- Backdrop & Detail Header -->
      <div class="relative bg-gradient-to-b from-[#222436] to-[#14151E] border-b border-white/10 pt-10 pb-12 px-4 lg:px-8">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-8 items-start">
          <!-- Poster -->
          <div class="w-48 sm:w-64 rounded-2xl overflow-hidden shadow-2xl border border-white/15 shrink-0 mx-auto md:mx-0">
            <img
              :src="content.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&q=80'"
              :alt="content.title"
              referrerpolicy="no-referrer"
              class="w-full h-auto object-cover"
            />
          </div>

          <!-- Info -->
          <div class="flex-1">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#F84464]/10 border border-[#F84464]/30 text-[#F84464] text-xs font-bold uppercase tracking-wider mb-3">
              {{ content.type === 'MOVIE' ? 'Movie Premiere' : 'Live Event' }} • {{ content.language }}
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              {{ content.title }}
            </h1>

            <div class="flex flex-wrap items-center gap-4 mt-3 text-xs sm:text-sm text-slate-300 font-medium">
              <span class="flex items-center gap-1 text-amber-400 font-bold">
                ★ {{ content.rating.toFixed(1) }} / 10
              </span>
              <span>•</span>
              <span>{{ Math.floor(content.duration_min / 60) }}h {{ content.duration_min % 60 }}m</span>
              <span>•</span>
              <span class="px-2.5 py-0.5 rounded bg-white/10 text-white">{{ content.genre }}</span>
            </div>

            <p class="text-slate-300 text-sm mt-4 leading-relaxed max-w-3xl">
              {{ content.description }}
            </p>

            <div class="mt-6 flex items-center gap-3">
              <div class="text-xs text-slate-400">
                City: <strong class="text-white">{{ cityStore.selectedCity }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Date Selector Tabs -->
      <div class="sticky top-[61px] z-30 bg-[#0F111A]/95 backdrop-blur-md border-b border-white/10 px-4 lg:px-8 py-3">
        <div class="max-w-7xl mx-auto flex items-center gap-3 overflow-x-auto pb-1">
          <button
            v-for="d in dateTabs"
            :key="d.dateStr"
            @click="selectedDate = d.dateStr"
            class="flex flex-col items-center min-w-[70px] py-2 px-3 rounded-xl border transition-all shrink-0"
            :class="
              selectedDate === d.dateStr
                ? 'bg-[#F84464] border-[#F84464] text-white shadow-lg shadow-[#F84464]/30'
                : 'bg-white/5 border-white/10 text-slate-300 hover:bg-white/10'
            "
          >
            <span class="text-[10px] uppercase font-bold tracking-wider">{{ d.dayLabel }}</span>
            <span class="text-sm font-extrabold mt-0.5">{{ d.dayNumber }}</span>
            <span class="text-[9px] text-white/80 font-medium">{{ d.monthLabel }}</span>
          </button>
        </div>
      </div>

      <!-- Theaters & Showtimes List -->
      <div class="max-w-7xl mx-auto px-4 lg:px-8 mt-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Theaters & Showtimes</span>
            <span class="text-xs font-normal text-slate-400">({{ theaterShows.length }} multiplexes)</span>
          </h2>
        </div>

        <div v-if="loadingShows" class="space-y-4">
          <div v-for="n in 3" :key="n" class="h-36 rounded-2xl bg-white/5 animate-pulse"></div>
        </div>

        <div v-else-if="theaterShows.length > 0" class="space-y-5">
          <div
            v-for="ts in theaterShows"
            :key="ts.theater_id"
            class="bms-card rounded-2xl p-5 border border-white/10 hover:border-white/20 transition-all shadow-xl"
          >
            <!-- Theater Header -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-white/10 gap-2">
              <div>
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                  <span>🏛️</span>
                  <span>{{ ts.theater_name }}</span>
                </h3>
                <p class="text-xs text-slate-400 mt-0.5">{{ ts.theater_address }}</p>
              </div>
              <div class="flex items-center gap-2 text-xs font-semibold text-emerald-400">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>Fast Filling</span>
              </div>
            </div>

            <!-- Showtimes Grid -->
            <div class="mt-4 flex flex-wrap items-center gap-3">
              <router-link
                v-for="show in ts.shows"
                :key="show.id"
                :to="`/shows/${show.id}/seats`"
                class="group px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 hover:border-[#F84464] hover:bg-[#F84464]/10 transition-all text-center flex flex-col items-center min-w-[110px]"
              >
                <span class="text-sm font-extrabold text-emerald-400 group-hover:text-[#F84464] transition-colors">
                  {{ formatShowTime(show.start_time) }}
                </span>
                <span class="text-[10px] font-semibold text-slate-400 mt-0.5">
                  {{ show.screen?.name || 'Screen' }}
                </span>
                <span class="text-[10px] font-bold text-slate-300 mt-1">
                  ₹{{ show.base_price.toFixed(0) }} onwards
                </span>
              </router-link>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-16 bg-white/5 rounded-2xl border border-white/10">
          <div class="text-3xl mb-2">🎟️</div>
          <h3 class="text-base font-bold text-white">No showtimes scheduled</h3>
          <p class="text-xs text-slate-400 mt-1">Please select a different date or check back later.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '../api/client'
import { useCityStore } from '../stores/city'

const route = useRoute()
const cityStore = useCityStore()

const contentId = route.params.id
const content = ref(null)
const theaterShows = ref([])
const loading = ref(true)
const loadingShows = ref(true)

// Generate next 7 days tabs
const dateTabs = ref([])
const selectedDate = ref('')

function initDateTabs() {
  const tabs = []
  const today = new Date()
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

  for (let i = 0; i < 7; i++) {
    const d = new Date()
    d.setDate(today.getDate() + i)
    const dateStr = d.toISOString().split('T')[0]
    tabs.push({
      dateStr,
      dayLabel: i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : days[d.getDay()],
      dayNumber: d.getDate(),
      monthLabel: months[d.getMonth()],
    })
  }
  dateTabs.value = tabs
  selectedDate.value = tabs[0].dateStr
}

async function fetchContentDetail() {
  loading.value = true
  try {
    const resp = await apiClient.get(`/content/${contentId}`)
    content.value = resp.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchShows() {
  loadingShows.value = true
  try {
    const resp = await apiClient.get('/shows', {
      params: {
        city: cityStore.selectedCity,
        date: selectedDate.value,
        content_id: contentId,
      },
    })
    theaterShows.value = resp.data
  } catch (err) {
    console.error(err)
  } finally {
    loadingShows.value = false
  }
}

function formatShowTime(isoString) {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })
}

watch(selectedDate, () => {
  fetchShows()
})

watch(
  () => cityStore.selectedCity,
  () => {
    fetchShows()
  }
)

onMounted(async () => {
  initDateTabs()
  await fetchContentDetail()
  await fetchShows()
})
</script>
