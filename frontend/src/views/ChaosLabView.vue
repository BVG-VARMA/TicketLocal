<template>
  <div class="min-h-screen pb-20 pt-8 px-4 lg:px-8">
    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span>⚡</span> Local Resilience Testing Engine
          </div>
          <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
            Chaos Engineering & Telemetry Lab
          </h1>
          <p class="text-xs sm:text-sm text-slate-400 mt-1">
            Simulate cache partitions, DB lock contention, tax calculation crashes, and concurrency storms.
          </p>
        </div>

        <button
          @click="chaosStore.resetChaos"
          :disabled="chaosStore.loading"
          class="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white text-xs font-bold transition-all shrink-0 flex items-center gap-2"
        >
          <span>🔄</span>
          <span>Reset All Faults</span>
        </button>
      </div>

      <!-- Real-Time Metrics Lite Cards -->
      <div>
        <h2 class="text-base font-bold text-white mb-4 flex items-center gap-2">
          <span>📊</span>
          <span>In-Process Metrics (metrics-lite)</span>
        </h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <div class="bms-card rounded-2xl p-4 border border-white/10 shadow-lg">
            <div class="text-[11px] font-semibold text-slate-400">Active Redis Locks</div>
            <div class="text-2xl font-black text-amber-400 font-mono mt-1">
              {{ chaosStore.metrics.active_redis_locks }}
            </div>
            <div class="text-[10px] text-slate-500 mt-1">Live 600s TTL holds</div>
          </div>

          <div class="bms-card rounded-2xl p-4 border border-white/10 shadow-lg">
            <div class="text-[11px] font-semibold text-slate-400">Seat Contentions (423)</div>
            <div class="text-2xl font-black text-rose-400 font-mono mt-1">
              {{ chaosStore.metrics.seat_contention_count_423 }}
            </div>
            <div class="text-[10px] text-slate-500 mt-1">Collisions prevented</div>
          </div>

          <div class="bms-card rounded-2xl p-4 border border-white/10 shadow-lg">
            <div class="text-[11px] font-semibold text-slate-400">Checkout Successes</div>
            <div class="text-2xl font-black text-emerald-400 font-mono mt-1">
              {{ chaosStore.metrics.checkout_success_count }}
            </div>
            <div class="text-[10px] text-slate-500 mt-1">Confirmed passes</div>
          </div>

          <div class="bms-card rounded-2xl p-4 border border-white/10 shadow-lg">
            <div class="text-[11px] font-semibold text-slate-400">Checkout Failures</div>
            <div class="text-2xl font-black text-rose-300 font-mono mt-1">
              {{ chaosStore.metrics.checkout_failed_count }}
            </div>
            <div class="text-[10px] text-slate-500 mt-1">Declines & conflicts</div>
          </div>

          <div class="bms-card rounded-2xl p-4 border border-white/10 shadow-lg">
            <div class="text-[11px] font-semibold text-slate-400">Abandonment Rate</div>
            <div class="text-2xl font-black text-cyan-400 font-mono mt-1">
              {{ chaosStore.metrics.checkout_abandonment_rate }}%
            </div>
            <div class="text-[10px] text-slate-500 mt-1">Attempts vs complete</div>
          </div>
        </div>
      </div>

      <!-- Fault Injection Action Panel -->
      <div>
        <h2 class="text-base font-bold text-white mb-4 flex items-center gap-2">
          <span>💥</span>
          <span>Fault Injection Triggers</span>
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <!-- 1. Redis Drop -->
          <div class="bms-card rounded-2xl p-5 border border-white/10 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white">1. Redis Lock Flush (Cache Wipe)</h3>
                <span class="text-xs px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                  Cache Drop
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-2 leading-relaxed">
                Flushes all active Redis seat locks. Tests if Postgres <code class="text-rose-300 font-mono text-[11px]">UNIQUE (show_id, seat_id)</code> constraint catches subsequent race condition checkouts with HTTP 409.
              </p>
            </div>
            <button
              @click="chaosStore.dropRedisLocks"
              :disabled="chaosStore.loading"
              class="mt-4 w-full py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold shadow-lg shadow-rose-600/30 transition-all"
            >
              Flush All Redis Locks
            </button>
          </div>

          <!-- 2. DB Lock Contention -->
          <div class="bms-card rounded-2xl p-5 border border-white/10 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white">2. DB Table Lock (5s Sleep)</h3>
                <span class="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  Deadlock Sim
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-2 leading-relaxed">
                Acquires an exclusive lock on the database tables and sleeps for 5 seconds to test async non-blocking execution and graceful statement timeout handling.
              </p>
            </div>
            <button
              @click="chaosStore.lockDatabase(5)"
              :disabled="chaosStore.loading"
              class="mt-4 w-full py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold shadow-lg shadow-amber-600/30 transition-all"
            >
              Lock DB for 5 Seconds
            </button>
          </div>

          <!-- 3. Tax Crash (ZeroDivisionError) -->
          <div class="bms-card rounded-2xl p-5 border border-white/10 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white">3. Tax Crash Fault Injection</h3>
                <span
                  class="text-xs px-2 py-0.5 rounded font-bold"
                  :class="chaosStore.status.tax_crash_active ? 'bg-rose-500/30 text-rose-300 border border-rose-500/50' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'"
                >
                  {{ chaosStore.status.tax_crash_active ? 'ACTIVE (CRASH)' : 'NORMAL' }}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-2 leading-relaxed">
                Forces <code class="text-amber-300 font-mono text-[11px]">ZeroDivisionError</code> during order totals calculation. Validates that checkout returns a clean HTTP 500 JSON payload instead of unhandled crashes.
              </p>
            </div>
            <button
              @click="chaosStore.toggleTaxCrash(!chaosStore.status.tax_crash_active)"
              :disabled="chaosStore.loading"
              class="mt-4 w-full py-2.5 rounded-xl text-white text-xs font-bold transition-all shadow-lg"
              :class="chaosStore.status.tax_crash_active ? 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-600/30' : 'bg-rose-600 hover:bg-rose-700 shadow-rose-600/30'"
            >
              {{ chaosStore.status.tax_crash_active ? 'Disable Tax Crash' : 'Enable Tax Crash (500 Error)' }}
            </button>
          </div>

          <!-- 4. QR Storm (Synchronous Blocking Stress) -->
          <div class="bms-card rounded-2xl p-5 border border-white/10 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-bold text-white">4. Synchronous QR Storm</h3>
                <span class="text-xs px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  CPU Bound
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-2 leading-relaxed">
                Generates 200 dense QR matrices in a loop to test event loop latency and prove why production ticket minting uses threadpool isolation.
              </p>
            </div>
            <button
              @click="chaosStore.triggerQrStorm(200)"
              :disabled="chaosStore.loading"
              class="mt-4 w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold shadow-lg shadow-purple-600/30 transition-all"
            >
              Launch QR Storm (200 QRs)
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useChaosStore } from '../stores/chaos'

const chaosStore = useChaosStore()
let metricsPollTimer = null

onMounted(async () => {
  await chaosStore.fetchStatus()
  await chaosStore.fetchMetrics()

  metricsPollTimer = setInterval(() => {
    chaosStore.fetchMetrics()
    chaosStore.fetchStatus()
  }, 2500)
})

onUnmounted(() => {
  if (metricsPollTimer) clearInterval(metricsPollTimer)
})
</script>
