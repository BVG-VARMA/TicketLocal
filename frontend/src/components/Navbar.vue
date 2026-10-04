<template>
  <nav class="sticky top-0 z-40 bg-[#0F111A]/90 backdrop-blur-md border-b border-white/10 px-4 lg:px-8 py-3.5 transition-all">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <!-- Logo & Brand -->
      <div class="flex items-center gap-8">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#F84464] to-[#FF6B8B] flex items-center justify-center text-white shadow-lg shadow-[#F84464]/30 group-hover:scale-105 transition-transform">
            <span class="text-xl font-black tracking-wider">TL</span>
          </div>
          <div>
            <div class="text-xl font-extrabold tracking-tight text-white flex items-center gap-1">
              Ticket<span class="text-[#F84464]">Local</span>
            </div>
            <div class="text-[10px] tracking-widest uppercase font-semibold text-slate-400">
              Direct Cinema & Live Passes
            </div>
          </div>
        </router-link>

        <!-- City Selector Button -->
        <button
          @click="cityStore.openCityModal()"
          class="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-white/5 border border-white/10 text-slate-200 hover:bg-white/10 hover:border-white/20 transition-all text-xs font-semibold"
        >
          <span class="text-[#F84464]">📍</span>
          <span>{{ cityStore.selectedCity }}</span>
          <span class="text-[10px] text-slate-400">▼</span>
        </button>
      </div>

      <!-- Center Links -->
      <div class="hidden md:flex items-center gap-6 text-sm font-medium">
        <router-link
          to="/"
          class="text-slate-300 hover:text-white transition-colors"
          active-class="text-[#F84464] font-semibold"
        >
          Movies
        </router-link>
        <router-link
          to="/?type=EVENT"
          class="text-slate-300 hover:text-white transition-colors"
        >
          Live Events
        </router-link>
        <router-link
          v-if="authStore.isAuthenticated"
          to="/bookings"
          class="text-slate-300 hover:text-white transition-colors"
          active-class="text-[#F84464] font-semibold"
        >
          My Bookings
        </router-link>
        <router-link
          to="/chaos"
          class="flex items-center gap-1.5 text-amber-400/90 hover:text-amber-300 transition-colors px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/20 text-xs font-semibold"
          active-class="bg-amber-500/20 text-amber-300 border-amber-500/40"
        >
          <span>⚡</span>
          <span>Chaos Lab</span>
        </router-link>
      </div>

      <!-- Right User Actions -->
      <div class="flex items-center gap-3">
        <!-- Mobile City Picker -->
        <button
          @click="cityStore.openCityModal()"
          class="sm:hidden px-2.5 py-1 rounded bg-white/5 border border-white/10 text-xs text-slate-200"
        >
          📍 {{ cityStore.selectedCity }}
        </button>

        <template v-if="authStore.isAuthenticated">
          <div class="flex items-center gap-3">
            <router-link
              to="/bookings"
              class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 text-xs font-semibold text-slate-200 transition-colors"
            >
              <span>🎟️</span>
              <span>Tickets</span>
            </router-link>
            <div class="flex items-center gap-2 pl-2 border-l border-white/10">
              <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-rose-500 to-amber-500 flex items-center justify-center font-bold text-xs text-white shadow">
                {{ (authStore.user?.name || 'U')[0].toUpperCase() }}
              </div>
              <button
                @click="authStore.logout()"
                class="text-xs text-slate-400 hover:text-rose-400 font-medium transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
        </template>

        <template v-else>
          <button
            @click="authStore.openLogin()"
            class="px-4 py-1.5 rounded-lg bg-[#F84464] hover:bg-[#e03353] text-white text-xs font-bold transition-all shadow-md shadow-[#F84464]/30 hover:scale-[1.02]"
          >
            Sign In
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useCityStore } from '../stores/city'

const authStore = useAuthStore()
const cityStore = useCityStore()
</script>
