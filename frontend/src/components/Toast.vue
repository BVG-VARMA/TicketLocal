<template>
  <div class="fixed top-20 right-5 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none">
    <transition-group
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-start gap-3 p-4 rounded-xl shadow-2xl border backdrop-blur-xl transition-all"
        :class="getToastClass(toast.type)"
      >
        <div class="shrink-0 mt-0.5">
          <span v-if="toast.type === 'success'" class="text-emerald-400 font-bold text-lg">✓</span>
          <span v-else-if="toast.type === 'error'" class="text-rose-400 font-bold text-lg">✕</span>
          <span v-else-if="toast.type === 'warning'" class="text-amber-400 font-bold text-lg">⚠</span>
          <span v-else class="text-cyan-400 font-bold text-lg">ℹ</span>
        </div>
        <div class="flex-1 text-sm font-medium leading-relaxed">
          {{ toast.message }}
        </div>
        <button
          @click="toastStore.remove(toast.id)"
          class="shrink-0 text-slate-400 hover:text-white transition-colors"
        >
          ✕
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

function getToastClass(type) {
  switch (type) {
    case 'success':
      return 'bg-emerald-950/90 border-emerald-500/30 text-emerald-100 shadow-emerald-950/50'
    case 'error':
      return 'bg-rose-950/90 border-rose-500/30 text-rose-100 shadow-rose-950/50'
    case 'warning':
      return 'bg-amber-950/90 border-amber-500/30 text-amber-100 shadow-amber-950/50'
    default:
      return 'bg-slate-900/90 border-slate-700/50 text-slate-100 shadow-slate-950/50'
  }
}
</script>
