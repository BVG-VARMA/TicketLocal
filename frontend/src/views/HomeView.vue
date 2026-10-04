<template>
  <div class="min-h-screen pb-16">
    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-b from-[#1E202E] to-[#14151E] border-b border-white/5 py-12 px-4 lg:px-8">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8">
        <div class="max-w-2xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#F84464]/10 border border-[#F84464]/30 text-[#F84464] text-xs font-bold uppercase tracking-wider mb-4">
            <span>✨</span> Live Booking in {{ cityStore.selectedCity }}
          </div>
          <h1 class="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Seamless Movie & Event Tickets in Real-Time
          </h1>
          <p class="text-slate-400 text-sm sm:text-base mt-3 leading-relaxed">
            Experience ultra-fast BookMyShow-style seat locking with sub-second Redis atomic holds, dynamic surge pricing, and instant QR passes.
          </p>
          <div class="flex flex-wrap items-center gap-3 mt-6">
            <button
              @click="activeType = 'MOVIE'"
              class="px-5 py-2.5 rounded-xl font-bold text-sm transition-all shadow-md"
              :class="activeType === 'MOVIE' ? 'bg-[#F84464] text-white shadow-[#F84464]/30' : 'bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10'"
            >
              🎬 Explore Movies
            </button>
            <button
              @click="activeType = 'EVENT'"
              class="px-5 py-2.5 rounded-xl font-bold text-sm transition-all shadow-md"
              :class="activeType === 'EVENT' ? 'bg-[#F84464] text-white shadow-[#F84464]/30' : 'bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10'"
            >
              🎤 Live Events & Concerts
            </button>
          </div>
        </div>

        <!-- Featured Spotlight Card -->
        <div class="w-full max-w-sm bms-card rounded-2xl p-4 border border-white/10 relative overflow-hidden shadow-2xl group">
          <div class="relative h-48 rounded-xl overflow-hidden mb-3">
            <img
              src="https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&q=80"
              alt="Spotlight"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-transparent"></div>
            <div class="absolute bottom-3 left-3 right-3 flex items-center justify-between">
              <span class="px-2.5 py-1 rounded bg-[#F84464] text-white text-xs font-bold">★ 9.1 / 10</span>
              <span class="text-xs font-semibold text-white/90">Sci-Fi • IMAX 4K</span>
            </div>
          </div>
          <h3 class="text-base font-bold text-white">Dune: Part Two</h3>
          <p class="text-xs text-slate-400 mt-1 line-clamp-2">
            Paul Atreides unites with Chani and the Fremen while seeking revenge against conspirators.
          </p>
        </div>
      </div>
    </div>

    <!-- Catalog Section -->
    <div class="max-w-7xl mx-auto px-4 lg:px-8 mt-10">
      <!-- Filter Bar -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/10 mb-8">
        <div>
          <h2 class="text-2xl font-black text-white flex items-center gap-2">
            <span>{{ activeType === 'MOVIE' ? 'Now Showing Movies' : 'Live Events & Specials' }}</span>
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-white/10 text-slate-300 font-mono font-normal">
              {{ filteredContent.length }} available
            </span>
          </h2>
          <p class="text-xs text-slate-400 mt-1">Showing verified schedules in {{ cityStore.selectedCity }}</p>
        </div>

        <!-- Search input -->
        <div class="relative w-full sm:w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search titles, genre..."
            class="w-full pl-9 pr-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-[#F84464] transition-colors"
          />
          <span class="absolute left-3 top-2.5 text-xs text-slate-400">🔍</span>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
        <div v-for="n in 8" :key="n" class="h-80 rounded-2xl bg-white/5 animate-pulse"></div>
      </div>

      <!-- Content Grid -->
      <div v-else-if="filteredContent.length > 0" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
        <div
          v-for="item in filteredContent"
          :key="item.id"
          class="bms-card rounded-2xl overflow-hidden border border-white/10 hover:border-[#F84464]/50 transition-all duration-300 group flex flex-col justify-between"
        >
          <!-- Poster -->
          <router-link :to="`/content/${item.id}`" class="block relative aspect-[2/3] overflow-hidden bg-slate-900">
            <img
              :src="item.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&q=80'"
              :alt="item.title"
              referrerpolicy="no-referrer"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-[#14151E] via-transparent to-transparent opacity-80"></div>

            <!-- Rating badge -->
            <div class="absolute bottom-3 left-3 px-2 py-1 rounded-md bg-black/80 backdrop-blur-md border border-white/10 flex items-center gap-1 text-xs font-bold text-amber-400">
              <span>★</span>
              <span>{{ item.rating.toFixed(1) }}</span>
            </div>

            <!-- Duration badge -->
            <div class="absolute bottom-3 right-3 px-2 py-1 rounded-md bg-black/80 backdrop-blur-md border border-white/10 text-[10px] font-semibold text-slate-300">
              {{ Math.floor(item.duration_min / 60) }}h {{ item.duration_min % 60 }}m
            </div>
          </router-link>

          <!-- Content Details -->
          <div class="p-4 flex-1 flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-2 text-[10px] font-bold uppercase tracking-wider text-[#F84464] mb-1">
                <span>{{ item.language }}</span>
                <span>•</span>
                <span class="text-slate-400">{{ item.genre }}</span>
              </div>
              <router-link
                :to="`/content/${item.id}`"
                class="text-sm sm:text-base font-bold text-white hover:text-[#F84464] transition-colors line-clamp-1"
              >
                {{ item.title }}
              </router-link>
              <p class="text-xs text-slate-400 mt-1 line-clamp-2">
                {{ item.description }}
              </p>
            </div>

            <router-link
              :to="`/content/${item.id}`"
              class="mt-4 w-full py-2.5 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white text-xs font-bold text-center transition-all shadow-md shadow-[#F84464]/20 group-hover:shadow-[#F84464]/40"
            >
              Book Tickets
            </router-link>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="text-4xl mb-2">🎬</div>
        <h3 class="text-lg font-bold text-white">No shows found</h3>
        <p class="text-xs text-slate-400 mt-1">Try changing your search query or city selection.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '../api/client'
import { useCityStore } from '../stores/city'

const route = useRoute()
const cityStore = useCityStore()

const activeType = ref(route.query.type === 'EVENT' ? 'EVENT' : 'MOVIE')
const searchQuery = ref('')
const contents = ref([])
const loading = ref(true)

watch(
  () => route.query.type,
  (newType) => {
    activeType.value = newType === 'EVENT' ? 'EVENT' : 'MOVIE'
  }
)

async function fetchContent() {
  loading.value = true
  try {
    const resp = await apiClient.get('/content')
    contents.value = resp.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const filteredContent = computed(() => {
  return contents.value.filter((item) => {
    const matchesType = item.type === activeType.value
    const matchesSearch =
      !searchQuery.value ||
      item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.genre.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesType && matchesSearch
  })
})

onMounted(() => {
  fetchContent()
})
</script>
