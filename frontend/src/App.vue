<template>
  <div class="min-h-screen bg-[#14151E] text-slate-100 flex flex-col antialiased selection:bg-[#F84464] selection:text-white">
    <!-- Navigation Bar -->
    <Navbar />

    <!-- Main View Content -->
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Global Toast Notifications -->
    <Toast />

    <!-- Modals -->
    <CityModal />
    <AuthModal />

    <!-- Footer -->
    <footer class="bg-[#0F111A] border-t border-white/10 py-8 px-4 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <span class="font-extrabold text-white">Ticket<span class="text-[#F84464]">Local</span></span>
          <span>• Production Movie & Live Event Booking Clone</span>
        </div>
        <div>
          <span>Local ACID Transactions (PostgreSQL) • Distributed 600s TTL (Redis) • SVG Curvature Seat Map</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import Toast from './components/Toast.vue'
import CityModal from './components/CityModal.vue'
import AuthModal from './components/AuthModal.vue'
import { useCityStore } from './stores/city'

const cityStore = useCityStore()

onMounted(() => {
  cityStore.fetchCities()
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
