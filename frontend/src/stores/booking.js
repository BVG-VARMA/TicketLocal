import { defineStore } from 'pinia'
import apiClient from '../api/client'
import { useToastStore } from './toast'
import { useAuthStore } from './auth'

export const useBookingStore = defineStore('booking', {
  state: () => ({
    currentShow: null,
    seatMatrix: null,
    selectedSeats: [], // Array of seat objects
    isHolding: false,
    holdsConfirmed: false,
    remainingSeconds: 600,
    timerInterval: null,
    cartQuote: null,
    loadingQuote: false,
    loadingCheckout: false,
    confirmedBooking: null,
  }),
  getters: {
    selectedSeatIds: (state) => state.selectedSeats.map((s) => s.id),
    subtotal: (state) => state.selectedSeats.reduce((acc, s) => acc + (s.computed_price || 0), 0),
    formattedTimer: (state) => {
      const mins = Math.floor(state.remainingSeconds / 60)
      const secs = state.remainingSeconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },
  },
  actions: {
    async fetchSeatMatrix(showId) {
      try {
        const resp = await apiClient.get(`/shows/${showId}/seats`)
        this.seatMatrix = resp.data
        return resp.data
      } catch (err) {
        const toast = useToastStore()
        toast.error('Failed to load seating matrix.')
        throw err
      }
    },
    toggleSeatSelection(seat) {
      if (seat.status === 'BOOKED') return
      if (seat.status === 'HELD' && !seat.held_by_me) return

      const toast = useToastStore()
      const existsIndex = this.selectedSeats.findIndex((s) => s.id === seat.id)

      if (existsIndex > -1) {
        this.selectedSeats.splice(existsIndex, 1)
      } else {
        if (this.selectedSeats.length >= 6) {
          toast.warning('Maximum 6 seats allowed per booking.')
          return
        }
        this.selectedSeats.push(seat)
      }
    },
    async holdSelectedSeats(showId) {
      const toast = useToastStore()
      const auth = useAuthStore()

      if (!auth.isAuthenticated) {
        auth.openLogin()
        toast.info('Please sign in to lock your seats.')
        return false
      }

      if (this.selectedSeats.length === 0) {
        toast.warning('Please select at least 1 seat.')
        return false
      }

      this.isHolding = true
      try {
        const resp = await apiClient.post(`/shows/${showId}/seats/hold`, {
          seat_ids: this.selectedSeatIds,
        })
        this.holdsConfirmed = true
        this.remainingSeconds = resp.data.ttl_seconds || 600
        this.startTimer(showId)
        toast.success(`Locked ${this.selectedSeats.length} seats for 10 minutes!`)
        return true
      } catch (err) {
        if (err.response?.status === 423) {
          const detail = err.response.data?.detail
          const msg = typeof detail === 'object' ? detail.message : detail || 'Selected seats are currently held by another user.'
          toast.error(msg)
          // Refresh matrix to show updated live locks
          await this.fetchSeatMatrix(showId)
          // Remove conflicting seats
          const conflicts = detail?.conflicting_seat_ids || []
          this.selectedSeats = this.selectedSeats.filter((s) => !conflicts.includes(s.id))
        } else {
          toast.error(err.response?.data?.detail || 'Failed to lock seats.')
        }
        return false
      } finally {
        this.isHolding = false
      }
    },
    startTimer(showId) {
      this.clearTimer()
      this.timerInterval = setInterval(() => {
        if (this.remainingSeconds > 0) {
          this.remainingSeconds--
        } else {
          this.handleTimerExpiry(showId)
        }
      }, 1000)
    },
    clearTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval)
        this.timerInterval = null
      }
    },
    async handleTimerExpiry(showId) {
      this.clearTimer()
      this.holdsConfirmed = false
      const toast = useToastStore()
      toast.warning('Seat reservation expired. Your holds have been released.')
      try {
        await apiClient.delete(`/shows/${showId}/seats/hold`)
      } catch (e) {
        // Ignored
      }
      this.selectedSeats = []
      await this.fetchSeatMatrix(showId)
    },
    async releaseHolds(showId) {
      this.clearTimer()
      if (this.holdsConfirmed && showId) {
        try {
          await apiClient.delete(`/shows/${showId}/seats/hold`, {
            data: { seat_ids: this.selectedSeatIds },
          })
        } catch (e) {
          // Ignored
        }
      }
      this.holdsConfirmed = false
      this.selectedSeats = []
    },
    async fetchCartQuote(showId) {
      this.loadingQuote = true
      const toast = useToastStore()
      try {
        const resp = await apiClient.post('/cart/quote', {
          show_id: showId,
          seat_ids: this.selectedSeatIds,
        })
        this.cartQuote = resp.data
        if (resp.data.min_remaining_ttl) {
          this.remainingSeconds = resp.data.min_remaining_ttl
        }
        return resp.data
      } catch (err) {
        toast.error('Failed to fetch pricing quote.')
        throw err
      } finally {
        this.loadingQuote = false
      }
    },
    async checkout(showId, paymentDetails) {
      this.loadingCheckout = true
      const toast = useToastStore()
      try {
        const resp = await apiClient.post('/checkout', {
          show_id: showId,
          seat_ids: this.selectedSeatIds,
          payment: paymentDetails,
        })
        this.confirmedBooking = resp.data
        this.clearTimer()
        this.holdsConfirmed = false
        this.selectedSeats = []
        toast.success('Payment successful! Your ticket is ready.')
        return { success: true, data: resp.data }
      } catch (err) {
        if (err.response?.status === 402) {
          toast.error('Payment declined by card gateway. Try using a valid test card.')
        } else if (err.response?.status === 409) {
          toast.error('Seat already booked in another transaction! Double-booking prevented.')
        } else if (err.response?.status === 423) {
          toast.error('Hold expired before payment. Please re-lock your seats.')
        } else if (err.response?.status === 500) {
          toast.error('Internal server error during order processing (Chaos tax crash active).')
        } else {
          toast.error(err.response?.data?.detail || 'Checkout failed.')
        }
        return { success: false, error: err }
      } finally {
        this.loadingCheckout = false
      }
    },
  },
})
