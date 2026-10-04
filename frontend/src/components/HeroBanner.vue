<template>
  <div v-if="movieList.length > 0" class="relative w-full my-6 select-none group">
    
    <!-- Carousel Frame -->
    <div class="relative w-full h-[360px] sm:h-[440px] md:h-[480px] overflow-hidden rounded-2xl sm:rounded-3xl border border-slate-800 shadow-2xl bg-[#1a1c26]">
      
      <!-- Backdrop Image -->
      <img 
        :src="currentMovie.backdrop_url || currentMovie.poster_url" 
        :alt="currentMovie.title"
        class="absolute inset-0 w-full h-full object-cover object-center filter brightness-[0.42] contrast-125 transition-all duration-700 group-hover:scale-105"
      />
      
      <!-- BookMyShow Gradient Overlays -->
      <div class="absolute inset-0 bg-gradient-to-t from-[#14151e] via-[#14151e]/60 to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-r from-[#14151e] via-[#14151e]/85 to-transparent"></div>

      <!-- Content Container -->
      <div class="absolute inset-0 p-6 sm:p-10 md:p-12 flex flex-col justify-end max-w-3xl z-10">
        
        <!-- Badges & Ratings -->
        <div class="flex flex-wrap items-center gap-2.5 mb-3">
          <span class="px-2.5 py-1 rounded-md bg-[#F84464] text-white font-black text-[11px] tracking-wider uppercase shadow-md">
            PREMIERE IN CINEMAS
          </span>
          <span class="px-2.5 py-1 rounded-md bg-slate-900/90 border border-slate-700 text-amber-400 text-xs font-bold flex items-center gap-1.5 shadow">
            <Star class="w-3.5 h-3.5 fill-amber-400" />
            <span>{{ currentMovie.rating }}/10</span>
            <span class="text-slate-400 font-normal text-[10px] hidden sm:inline">(142.8K Votes)</span>
          </span>
          <span class="px-2 py-0.8 rounded-md bg-slate-900/90 border border-slate-700 text-slate-300 text-xs font-semibold">
            {{ currentMovie.certificate }}
          </span>
          <span class="px-2 py-0.8 rounded-md bg-slate-900/90 border border-slate-700 text-slate-300 text-xs font-semibold">
            {{ currentMovie.duration_min }} mins
          </span>
        </div>

        <!-- Movie Title -->
        <h1 class="text-2xl sm:text-4xl md:text-5xl font-black text-white tracking-tight leading-tight mb-2 drop-shadow-lg">
          {{ currentMovie.title }}
        </h1>

        <!-- Formats & Languages -->
        <p class="text-xs sm:text-sm text-slate-300 font-medium mb-3 flex items-center gap-2.5">
          <span class="text-[#F84464] font-bold">{{ currentMovie.languages }}</span>
          <span class="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
          <span>{{ currentMovie.genres }}</span>
          <span class="w-1.5 h-1.5 rounded-full bg-slate-600 hidden sm:inline-block"></span>
          <span class="text-amber-400 text-xs font-bold hidden sm:inline-block">2D, 3D, IMAX 3D, 4DX</span>
        </p>

        <!-- Synopsis -->
        <p class="text-xs sm:text-sm text-slate-400 line-clamp-2 max-w-2xl mb-6 leading-relaxed hidden sm:block">
          {{ currentMovie.synopsis }}
        </p>

        <!-- Call to Action Buttons -->
        <div class="flex items-center gap-3 sm:gap-4">
          <button
            @click="$emit('select-movie', currentMovie)"
            class="flex items-center gap-2 px-6 sm:px-8 py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-sm sm:text-base shadow-lg shadow-[#F84464]/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <Ticket class="w-4 h-4 sm:w-5 sm:h-5 stroke-[2.2]" />
            <span>Book Tickets</span>
          </button>

          <button
            @click="$emit('select-movie', currentMovie)"
            class="flex items-center gap-2 px-4 sm:px-5 py-3 rounded-xl bg-slate-900/80 border border-slate-700 hover:border-slate-500 text-slate-200 font-semibold text-xs sm:text-sm transition-all"
          >
            <PlayCircle class="w-4 h-4 sm:w-5 sm:h-5 text-[#F84464]" />
            <span>Watch Trailer</span>
          </button>
        </div>

      </div>

      <!-- Left / Right Carousel Controls -->
      <button 
        @click="prevSlide"
        class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/60 hover:bg-[#F84464] text-white flex items-center justify-center transition-all opacity-0 group-hover:opacity-100 z-20"
      >
        <ChevronLeft class="w-6 h-6" />
      </button>

      <button 
        @click="nextSlide"
        class="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/60 hover:bg-[#F84464] text-white flex items-center justify-center transition-all opacity-0 group-hover:opacity-100 z-20"
      >
        <ChevronRight class="w-6 h-6" />
      </button>

      <!-- Carousel Dot Indicators -->
      <div class="absolute bottom-4 right-6 sm:right-10 flex items-center gap-2 z-20">
        <button
          v-for="(m, idx) in movieList"
          :key="m.id"
          @click="currentIndex = idx"
          class="h-2 rounded-full transition-all duration-300"
          :class="currentIndex === idx ? 'w-6 bg-[#F84464]' : 'w-2 bg-slate-600 hover:bg-slate-400'"
        ></button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Star, Ticket, PlayCircle, ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  featuredMovie: { type: Object, default: null },
  movies: { type: Array, default: () => [] }
})

defineEmits(['select-movie'])

const currentIndex = ref(0)
let timer = null

const movieList = computed(() => {
  if (props.movies && props.movies.length > 0) {
    return props.movies.slice(0, 5)
  }
  return props.featuredMovie ? [props.featuredMovie] : []
})

const currentMovie = computed(() => {
  return movieList.value[currentIndex.value] || props.featuredMovie
})

const nextSlide = () => {
  if (movieList.value.length === 0) return
  currentIndex.value = (currentIndex.value + 1) % movieList.value.length
}

const prevSlide = () => {
  if (movieList.value.length === 0) return
  currentIndex.value = (currentIndex.value - 1 + movieList.value.length) % movieList.value.length
}

onMounted(() => {
  timer = setInterval(nextSlide, 5000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>
