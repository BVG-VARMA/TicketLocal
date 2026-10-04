<template>
  <div class="my-6 space-y-10">
    
    <!-- Recommended Movies Section (BMS Style) -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-2xl font-black text-white tracking-tight">
              Recommended Movies
            </h2>
            <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium hidden sm:inline">
              in {{ currentCity }}
            </span>
          </div>
          <p class="text-xs text-slate-400 mt-0.5">Explore the latest blockbuster releases and book instant seats</p>
        </div>

        <!-- Filter Chips (Languages & Genres) -->
        <div class="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
          <button
            v-for="genre in genreFilters"
            :key="genre"
            @click="selectedGenre = genre"
            class="px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap transition-all"
            :class="selectedGenre === genre ? 'bg-[#F84464] text-white shadow-md' : 'bg-slate-800/80 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700'"
          >
            {{ genre }}
          </button>
        </div>
      </div>

      <!-- Movie Cards Grid (BookMyShow Authentic Ratio) -->
      <div v-if="filteredMovies.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 sm:gap-6">
        <div
          v-for="movie in filteredMovies"
          :key="movie.id"
          @click="$emit('select-movie', movie)"
          class="group bms-card rounded-2xl overflow-hidden bms-card-hover cursor-pointer flex flex-col justify-between select-none"
        >
          <!-- Poster Container -->
          <div class="relative aspect-[2/3] overflow-hidden bg-slate-900 rounded-t-2xl">
            <img 
              :src="movie.poster_url" 
              :alt="movie.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />

            <!-- BookMyShow Rating Strip at Bottom of Poster -->
            <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black via-black/90 to-transparent p-2 pt-6 flex items-center justify-between text-xs">
              <div class="flex items-center gap-1.5 text-white font-bold">
                <Star class="w-3.5 h-3.5 text-[#F84464] fill-[#F84464]" />
                <span>{{ movie.rating }}/10</span>
                <span class="text-[10px] text-slate-400 font-normal">({{ Math.floor(movie.rating * 14.5) }}K Votes)</span>
              </div>
            </div>

            <!-- Format Badge Top-Left -->
            <div class="absolute top-2.5 left-2.5">
              <span class="px-2 py-0.5 rounded bg-black/75 backdrop-blur-md border border-slate-700/80 text-[10px] font-black text-amber-400 tracking-wider">
                IMAX 3D
              </span>
            </div>

            <!-- Hover "Book Tickets" Overlay -->
            <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center p-4">
              <span class="px-4 py-2 rounded-xl bg-[#F84464] text-white font-bold text-xs shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-transform">
                Book Tickets
              </span>
            </div>
          </div>

          <!-- Movie Metadata -->
          <div class="p-3.5 flex-1 flex flex-col justify-between space-y-2">
            <div>
              <h3 class="font-bold text-sm text-white line-clamp-1 group-hover:text-[#F84464] transition-colors">
                {{ movie.title }}
              </h3>
              <p class="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                {{ movie.genres }}
              </p>
            </div>

            <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
              <span class="px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-semibold text-[10px]">
                {{ movie.certificate }}
              </span>
              <span class="text-[#F84464] font-semibold truncate max-w-[120px]">
                {{ movie.languages }}
              </span>
            </div>
          </div>

        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="bms-card rounded-2xl p-12 text-center my-6">
        <Film class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <h3 class="text-base font-bold text-slate-300">No movies found for this filter</h3>
        <p class="text-xs text-slate-500 mt-1">Try selecting 'All' or a different city.</p>
      </div>
    </div>

    <!-- BookMyShow Stream Promo Ribbon -->
    <div class="rounded-2xl bg-gradient-to-r from-[#2c1320] via-[#1a1b29] to-[#0f192b] border border-rose-900/40 p-5 sm:p-6 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-[#F84464] flex items-center justify-center shrink-0 shadow-lg shadow-[#F84464]/30">
          <Play class="w-6 h-6 text-white fill-white ml-0.5" />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-lg font-black text-white">book<span class="text-[#F84464]">my</span>show</span>
            <span class="px-2 py-0.5 rounded bg-[#F84464] text-white text-[10px] font-black uppercase">STREAM</span>
          </div>
          <p class="text-xs text-slate-300 mt-0.5">Endless Entertainment. Anytime. Anywhere. Rent or buy the biggest blockbusters.</p>
        </div>
      </div>
      <button class="px-5 py-2.5 rounded-xl bg-white hover:bg-slate-100 text-slate-950 font-bold text-xs shrink-0 transition-colors shadow">
        Explore Stream
      </button>
    </div>

    <!-- The Best of Live Events (BMS Live Strip) -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-white tracking-tight">The Best of Live Events</h2>
        <span class="text-xs text-[#F84464] font-semibold hover:underline cursor-pointer">See All ›</span>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div 
          v-for="ev in liveEvents" 
          :key="ev.title"
          class="bms-card rounded-2xl p-4 border border-slate-800 hover:border-[#F84464]/50 transition-all cursor-pointer group"
        >
          <div class="text-3xl mb-2">{{ ev.icon }}</div>
          <h4 class="font-bold text-sm text-white group-hover:text-[#F84464] transition-colors">{{ ev.title }}</h4>
          <p class="text-[11px] text-slate-400 mt-0.5">{{ ev.subtitle }}</p>
          <span class="inline-block mt-3 text-[10px] font-bold text-amber-400">{{ ev.tag }}</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Star, Film, Play } from 'lucide-vue-next'

const props = defineProps({
  movies: { type: Array, default: () => [] },
  currentCity: { type: String, default: 'Hyderabad' }
})

defineEmits(['select-movie'])

const genreFilters = ['All', 'Action', 'Sci-Fi', 'Horror', 'Drama', 'Adventure', 'Thriller']
const selectedGenre = ref('All')

const filteredMovies = computed(() => {
  if (selectedGenre.value === 'All') return props.movies
  return props.movies.filter(m => m.genres.toLowerCase().includes(selectedGenre.value.toLowerCase()))
})

const liveEvents = [
  { title: 'Standup Comedy Special', subtitle: 'Live Standup & Open Mics', icon: '🎙️', tag: '35+ Events' },
  { title: 'Music Concerts & Festivals', subtitle: 'Sunburn & Acoustic Nights', icon: '🎸', tag: '20+ Events' },
  { title: 'Theatre & Broadway Plays', subtitle: 'Classic Dramas & Adaptations', icon: '🎭', tag: '12+ Plays' },
  { title: 'IPL & Sports Matches', subtitle: 'Stadium Tickets & Fan Parks', icon: '🏏', tag: 'Filling Fast' },
]
</script>
