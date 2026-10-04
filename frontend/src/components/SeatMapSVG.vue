<template>
  <div class="w-full flex flex-col items-center select-none">
    <!-- Cinema Curved Screen Banner -->
    <div class="w-full max-w-3xl flex flex-col items-center mb-8 relative">
      <svg class="w-full h-14 overflow-visible" viewBox="0 0 800 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="screenGlow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#F84464" stop-opacity="0.1" />
            <stop offset="50%" stop-color="#F84464" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#F84464" stop-opacity="0.1" />
          </linearGradient>
          <filter id="blurGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>
        <!-- Curved Screen Line -->
        <path
          d="M 50 45 Q 400 5 750 45"
          stroke="url(#screenGlow)"
          stroke-width="5"
          stroke-linecap="round"
          filter="url(#blurGlow)"
        />
        <path
          d="M 50 45 Q 400 5 750 45"
          stroke="#FFFFFF"
          stroke-width="2"
          stroke-linecap="round"
        />
      </svg>
      <div class="text-[11px] font-bold tracking-widest text-slate-400 uppercase -mt-2">
        All Eyes This Way • Cinema Screen
      </div>
    </div>

    <!-- SVG Interactive Seating Grid -->
    <div class="w-full overflow-x-auto pb-6 flex justify-center">
      <svg
        :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
        :style="{ width: `${Math.min(svgWidth, 860)}px`, minWidth: '600px' }"
        class="overflow-visible"
      >
        <g v-for="(row, rIdx) in rows" :key="row.row_label">
          <!-- Row Label Left -->
          <text
            :x="25"
            :y="getY(rIdx) + 20"
            fill="#94A3B8"
            font-size="13"
            font-weight="700"
            text-anchor="middle"
          >
            {{ row.row_label }}
          </text>

          <!-- Seat Items -->
          <g
            v-for="(seat, sIdx) in row.seats"
            :key="seat.id"
            class="cursor-pointer transition-transform"
            @click="handleSeatClick(seat)"
          >
            <!-- Seat Outline & Fill -->
            <rect
              :x="getX(sIdx, seat.seat_number)"
              :y="getY(rIdx)"
              width="28"
              height="28"
              rx="6"
              :class="getSeatClasses(seat)"
              :stroke="getSeatStroke(seat)"
              stroke-width="1.5"
            />

            <!-- Seat Number inside rect -->
            <text
              :x="getX(sIdx, seat.seat_number) + 14"
              :y="getY(rIdx) + 18"
              :fill="getTextColor(seat)"
              font-size="10"
              font-weight="700"
              text-anchor="middle"
              class="pointer-events-none select-none"
            >
              {{ seat.seat_number }}
            </text>

            <!-- Held Indicator Icon (Pulsing Lock) -->
            <circle
              v-if="seat.status === 'HELD'"
              :cx="getX(sIdx, seat.seat_number) + 24"
              :cy="getY(rIdx) + 4"
              r="4"
              class="fill-amber-400 animate-pulse"
            />
          </g>

          <!-- Row Label Right -->
          <text
            :x="svgWidth - 25"
            :y="getY(rIdx) + 20"
            fill="#94A3B8"
            font-size="13"
            font-weight="700"
            text-anchor="middle"
          >
            {{ row.row_label }}
          </text>
        </g>
      </svg>
    </div>

    <!-- Color Legend -->
    <div class="w-full max-w-2xl bg-white/5 border border-white/10 rounded-xl p-4 mt-2 flex flex-wrap items-center justify-around gap-4 text-xs font-semibold text-slate-300">
      <div class="flex items-center gap-2">
        <div class="w-5 h-5 rounded-md bg-[#1E293B] border border-slate-600"></div>
        <span>Available</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-5 h-5 rounded-md bg-[#F84464] border border-[#F84464] shadow-sm shadow-[#F84464]/50"></div>
        <span>Selected (You)</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-5 h-5 rounded-md bg-amber-500/20 border border-amber-500 animate-pulse"></div>
        <span>Held (10m Lock)</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-5 h-5 rounded-md bg-slate-800 border border-slate-800 opacity-40"></div>
        <span class="text-slate-500">Booked</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  rows: {
    type: Array,
    required: true,
  },
  selectedSeatIds: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['toggle-seat'])

const maxCols = computed(() => {
  if (!props.rows || props.rows.length === 0) return 12
  return Math.max(...props.rows.map((r) => r.seats.length))
})

const svgWidth = computed(() => {
  // Margins 70 + (col width 36 * maxCols) + walkway 40 + margin 70
  return 140 + maxCols.value * 38 + 40
})

const svgHeight = computed(() => {
  return props.rows.length * 42 + 40
})

function getX(colIdx, seatNum) {
  const startX = 65
  const colWidth = 38
  // Add walkway gap in the middle
  const walkwayGap = seatNum > Math.floor(maxCols.value / 2) ? 36 : 0
  return startX + colIdx * colWidth + walkwayGap
}

function getY(rowIdx) {
  const startY = 20
  const rowHeight = 42
  return startY + rowIdx * rowHeight
}

function isSelected(seat) {
  return props.selectedSeatIds.includes(seat.id)
}

function handleSeatClick(seat) {
  if (seat.status === 'BOOKED') return
  if (seat.status === 'HELD' && !seat.held_by_me) return
  emit('toggle-seat', seat)
}

function getSeatClasses(seat) {
  if (isSelected(seat)) {
    return 'fill-[#F84464] hover:scale-105 transition-transform duration-150'
  }
  if (seat.status === 'BOOKED') {
    return 'fill-slate-800/60 opacity-40 cursor-not-allowed'
  }
  if (seat.status === 'HELD') {
    if (seat.held_by_me) {
      return 'fill-[#F84464]/80 animate-pulse cursor-pointer'
    }
    return 'fill-amber-500/20 cursor-not-allowed'
  }

  // AVAILABLE - tier colors
  if (seat.seat_type === 'RECLINER') {
    return 'fill-amber-950/60 hover:fill-amber-600/50 hover:scale-105 transition-transform duration-150'
  }
  if (seat.seat_type === 'PREMIUM') {
    return 'fill-purple-950/60 hover:fill-purple-600/50 hover:scale-105 transition-transform duration-150'
  }
  return 'fill-slate-800/80 hover:fill-slate-700 hover:scale-105 transition-transform duration-150'
}

function getSeatStroke(seat) {
  if (isSelected(seat)) return '#FFFFFF'
  if (seat.status === 'BOOKED') return '#1E293B'
  if (seat.status === 'HELD') return '#F59E0B'

  if (seat.seat_type === 'RECLINER') return '#D97706'
  if (seat.seat_type === 'PREMIUM') return '#9333EA'
  return '#475569'
}

function getTextColor(seat) {
  if (isSelected(seat)) return '#FFFFFF'
  if (seat.status === 'BOOKED') return '#475569'
  if (seat.status === 'HELD') return '#F59E0B'
  return '#E2E8F0'
}
</script>
