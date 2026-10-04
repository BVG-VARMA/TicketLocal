<template>
  <div
    v-if="cityStore.isCityModalOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm transition-all"
    @click.self="cityStore.closeCityModal()"
  >
    <div class="w-full max-w-md bg-[#181A24] border border-white/10 rounded-2xl p-6 shadow-2xl animate-in fade-in zoom-in duration-200">
      <div class="flex items-center justify-between pb-4 border-b border-white/10 mb-5">
        <div>
          <h3 class="text-lg font-bold text-white">Select City</h3>
          <p class="text-xs text-slate-400 mt-0.5">Explore movies & shows near you</p>
        </div>
        <button
          @click="cityStore.closeCityModal()"
          class="text-slate-400 hover:text-white text-lg transition-colors"
        >
          ✕
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <button
          v-for="city in cityStore.cities"
          :key="city.id"
          @click="cityStore.setCity(city.name)"
          class="flex flex-col items-center justify-center p-4 rounded-xl border transition-all text-center group"
          :class="
            cityStore.selectedCity === city.name
              ? 'bg-[#F84464]/10 border-[#F84464] text-white shadow-lg shadow-[#F84464]/20'
              : 'bg-white/5 border-white/5 text-slate-300 hover:bg-white/10 hover:border-white/15'
          "
        >
          <span class="text-2xl mb-1 group-hover:scale-110 transition-transform">
            {{ city.name === 'Hyderabad' ? '🏛️' : city.name === 'Bangalore' ? '🏢' : '🌊' }}
          </span>
          <span class="text-sm font-semibold">{{ city.name }}</span>
          <span
            v-if="cityStore.selectedCity === city.name"
            class="text-[10px] text-[#F84464] font-bold mt-1 uppercase tracking-wider"
          >
            Selected
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCityStore } from '../stores/city'

const cityStore = useCityStore()
</script>
