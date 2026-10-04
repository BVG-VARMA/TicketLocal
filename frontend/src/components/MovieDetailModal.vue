<template>
  <div v-if="movie" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/85 backdrop-blur-md">
    <div class="bg-[#1a1c26] w-full max-w-5xl rounded-3xl border border-slate-700/80 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200 my-auto flex flex-col max-h-[92vh]">
      
      <!-- Modal Header Banner (BMS Style) -->
      <div class="relative h-60 sm:h-72 shrink-0 overflow-hidden bg-[#11121a]">
        <img 
          :src="movie.backdrop_url || movie.poster_url" 
          :alt="movie.title"
          class="w-full h-full object-cover filter brightness-[0.45] scale-105"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-[#1a1c26] via-[#1a1c26]/50 to-transparent"></div>

        <!-- Close Button -->
        <button 
          @click="$emit('close')"
          class="absolute top-4 right-4 p-2 rounded-full bg-black/70 hover:bg-[#F84464] text-slate-300 hover:text-white transition-all border border-slate-700 z-20"
        >
          <X class="w-5 h-5" />
        </button>

        <!-- Movie Info Overlay -->
        <div class="absolute bottom-5 left-6 right-6 flex items-end gap-5 z-10">
          <img 
            :src="movie.poster_url" 
            :alt="movie.title"
            class="w-24 sm:w-32 rounded-xl border-2 border-slate-700 shadow-2xl shrink-0 hidden sm:block aspect-[2/3] object-cover"
          />
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <span class="px-2.5 py-0.5 rounded bg-[#F84464] text-white font-black text-[11px] uppercase tracking-wider">
                {{ movie.certificate }}
              </span>
              <span class="text-xs text-amber-400 font-bold flex items-center gap-1 bg-slate-900/90 px-2 py-0.5 rounded border border-slate-700">
                <Star class="w-3.5 h-3.5 fill-amber-400" />
                {{ movie.rating }}/10
                <span class="text-slate-400 font-normal text-[10px] hidden sm:inline">(142.8K Votes)</span>
              </span>
              <span class="text-xs text-slate-300 font-medium bg-slate-900/90 px-2 py-0.5 rounded border border-slate-700">
                {{ movie.duration_min }} mins
              </span>
            </div>
            
            <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight">
              {{ movie.title }}
            </h2>
            
            <p class="text-xs sm:text-sm text-slate-300 mt-1 flex flex-wrap items-center gap-2">
              <span class="text-[#F84464] font-semibold">{{ movie.languages }}</span>
              <span>•</span>
              <span>{{ movie.genres }}</span>
              <span>•</span>
              <span class="text-amber-400 font-bold">2D, 3D, IMAX 3D, 4DX</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Modal Body (Scrollable Showtimes) -->
      <div class="flex-1 overflow-y-auto p-5 sm:p-6 space-y-6">

        <!-- Synopsis & About -->
        <div class="bg-[#222434]/60 p-4 rounded-2xl border border-slate-800">
          <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">About the Movie</h3>
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">{{ movie.synopsis }}</p>
        </div>

        <!-- BookMyShow Horizontal Date Selector Bar -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <Calendar class="w-4 h-4 text-[#F84464]" />
              <span>Select Show Date</span>
            </h3>
            <span class="text-xs text-slate-400">Cinemas in <strong class="text-white">{{ city }}</strong></span>
          </div>

          <div class="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-none">
            <button
              v-for="d in dateList"
              :key="d.date"
              @click="selectedDate = d.date; fetchShows()"
              class="flex flex-col items-center px-4 py-2.5 rounded-2xl border text-center transition-all min-w-[95px] select-none"
              :class="selectedDate === d.date ? 'bg-[#F84464] border-[#F84464] text-white shadow-lg shadow-[#F84464]/30 font-bold' : 'bg-[#222434] border-slate-700 text-slate-400 hover:text-white hover:border-slate-500'"
            >
              <span class="text-[10px] uppercase tracking-wider font-bold">{{ d.dayLabel }}</span>
              <span class="text-lg font-black leading-none my-0.5">{{ d.dayNum }}</span>
              <span class="text-[10px] font-medium uppercase">{{ d.month }}</span>
            </button>
          </div>
        </div>

        <!-- Cinema Listings & Showtimes (BMS Theater Cards) -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <MapPin class="w-4 h-4 text-[#F84464]" />
              <span>Available Theaters & Screen Formats</span>
            </h3>
            
            <!-- Availability Color Legend -->
            <div class="hidden sm:flex items-center gap-4 text-[11px] text-slate-400">
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> Available</span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Fast Filling</span>
            </div>
          </div>

          <div v-if="loadingShows" class="py-16 text-center text-slate-400 text-sm">
            <div class="w-7 h-7 border-2 border-[#F84464] border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
            Loading available cinema showtimes in {{ city }}...
          </div>

          <div v-else-if="groupedTheaters.length > 0" class="space-y-4">
            <div 
              v-for="theater in groupedTheaters" 
              :key="theater.id"
              class="bg-[#222434]/80 p-4 sm:p-5 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-slate-700 transition-colors"
            >
              <!-- Theater Information -->
              <div class="max-w-xs sm:max-w-sm">
                <div class="flex items-center gap-2">
                  <Heart class="w-4 h-4 text-slate-500 hover:text-[#F84464] cursor-pointer transition-colors" />
                  <h4 class="font-bold text-sm text-white">{{ theater.name }}</h4>
                </div>
                <p class="text-xs text-slate-400 mt-1 line-clamp-1">{{ theater.address }}</p>
                <div class="flex items-center gap-2 mt-2 text-[10px]">
                  <span class="px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800 font-semibold flex items-center gap-1">
                    <Smartphone class="w-3 h-3" /> M-Ticket
                  </span>
                  <span class="px-2 py-0.5 rounded bg-amber-950/60 text-amber-400 border border-amber-800 font-semibold flex items-center gap-1">
                    <Coffee class="w-3 h-3" /> F&B Available
                  </span>
                </div>
              </div>

              <!-- Showtime Buttons (BookMyShow Style) -->
              <div class="flex flex-wrap items-center gap-3">
                <button
                  v-for="(show, sIdx) in theater.shows"
                  :key="show.id"
                  @click="$emit('select-show', show)"
                  class="group px-4 py-2.5 rounded-xl border text-center transition-all flex flex-col items-center justify-center min-w-[100px] hover:scale-105 active:scale-95"
                  :class="sIdx % 2 === 0 ? 'bg-slate-900/90 border-emerald-500/50 hover:border-emerald-400 text-emerald-400 hover:bg-emerald-500/10' : 'bg-slate-900/90 border-amber-500/50 hover:border-amber-400 text-amber-400 hover:bg-amber-500/10'"
                >
                  <span class="text-xs font-black tracking-wide">{{ show.start_time }}</span>
                  <span class="text-[9px] text-slate-400 font-semibold uppercase mt-0.5">
                    {{ show.format }}
                  </span>
                  <span class="text-[9px] text-slate-500 font-mono mt-0.5">
                    ₹{{ show.price_range?.CLASSIC || 180 }}+
                  </span>
                </button>
              </div>
            </div>
          </div>

          <!-- Empty Showtimes State -->
          <div v-else class="bg-[#222434]/40 p-12 rounded-2xl text-center text-slate-400 text-sm border border-slate-800">
            <Film class="w-10 h-10 text-slate-600 mx-auto mb-2" />
            <p class="font-bold text-slate-300">No showtimes available for the selected date.</p>
            <p class="text-xs text-slate-500 mt-1">Please select another date above or change your city.</p>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { X, Star, Calendar, MapPin, Heart, Smartphone, Coffee, Film } from 'lucide-vue-next'
import { api } from '../services/api'

const props = defineProps({
  movie: { type: Object, default: null },
  city: { type: String, default: 'Hyderabad' }
})

const emit = defineEmits(['close', 'select-show'])

const loadingShows = ref(false)
const showsList = ref([])

// Generate date choices (Today + next 4 days)
const dateList = computed(() => {
  const dates = []
  const today = new Date()
  for (let i = 0; i < 5; i++) {
    const d = new Date(today)
    d.setDate(today.getDate() + i)
    const isoDate = d.toISOString().split('T')[0]
    const dayLabel = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : d.toLocaleDateString('en-US', { weekday: 'short' })
    dates.push({
      date: isoDate,
      dayLabel: dayLabel,
      dayNum: d.getDate(),
      month: d.toLocaleDateString('en-US', { month: 'short' })
    })
  }
  return dates
})

const selectedDate = ref(dateList.value[0]?.date || '')

async function fetchShows() {
  if (!props.movie) return
  loadingShows.value = true
  try {
    showsList.value = await api.getShows({
      city: props.city,
      date: selectedDate.value,
      movie_id: props.movie.id
    })
  } catch (e) {
    console.error('Failed to fetch shows:', e)
  } finally {
    loadingShows.value = false
  }
}

// Group shows by theater
const groupedTheaters = computed(() => {
  const map = {}
  for (const show of showsList.value) {
    const t = show.theater
    if (!t) continue
    if (!map[t.id]) {
      map[t.id] = {
        id: t.id,
        name: t.name,
        address: t.address,
        amenities: t.amenities,
        shows: []
      }
    }
    map[t.id].shows.push(show)
  }
  return Object.values(map)
})

onMounted(() => {
  fetchShows()
})
</script>
