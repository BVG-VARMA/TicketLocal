import { defineStore } from 'pinia'
import apiClient from '../api/client'
import { useToastStore } from './toast'

export const useChaosStore = defineStore('chaos', {
  state: () => ({
    status: {
      chaos_enabled: true,
      tax_crash_active: false,
      db_lock_active: false,
    },
    metrics: {
      active_redis_locks: 0,
      seat_contention_count_423: 0,
      checkout_success_count: 0,
      checkout_failed_count: 0,
      checkout_abandonment_rate: 0,
      uptime_seconds: 0,
    },
    loading: false,
  }),
  actions: {
    async fetchStatus() {
      try {
        const resp = await apiClient.get('/chaos/status')
        this.status = resp.data
      } catch (e) {
        // Chaos might be disabled
      }
    },
    async fetchMetrics() {
      try {
        const resp = await apiClient.get('/metrics-lite')
        this.metrics = resp.data
      } catch (e) {
        // Ignore
      }
    },
    async dropRedisLocks() {
      this.loading = true
      const toast = useToastStore()
      try {
        const resp = await apiClient.post('/chaos/redis-drop')
        toast.warning(resp.data.message || 'Wiped all Redis seat locks!')
        await this.fetchMetrics()
      } catch (e) {
        toast.error('Failed to execute redis drop.')
      } finally {
        this.loading = false
      }
    },
    async lockDatabase(seconds = 5) {
      this.loading = true
      const toast = useToastStore()
      try {
        toast.info(`Acquiring database lock for ${seconds} seconds...`)
        const resp = await apiClient.post(`/chaos/db-lock?sleep_seconds=${seconds}`)
        toast.success(resp.data.message)
        await this.fetchStatus()
      } catch (e) {
        toast.error('Failed to lock database.')
      } finally {
        this.loading = false
      }
    },
    async toggleTaxCrash(enable) {
      this.loading = true
      const toast = useToastStore()
      try {
        const resp = await apiClient.post(`/chaos/tax-crash?enable=${enable}`)
        this.status.tax_crash_active = resp.data.tax_crash_active
        toast.warning(resp.data.message)
      } catch (e) {
        toast.error('Failed to toggle tax crash.')
      } finally {
        this.loading = false
      }
    },
    async triggerQrStorm(count = 200) {
      this.loading = true
      const toast = useToastStore()
      try {
        toast.info(`Triggering synchronous QR storm (${count} items)...`)
        const resp = await apiClient.post(`/chaos/qr-storm?count=${count}`)
        toast.warning(resp.data.message)
      } catch (e) {
        toast.error('QR storm failed.')
      } finally {
        this.loading = false
      }
    },
    async resetChaos() {
      this.loading = true
      const toast = useToastStore()
      try {
        const resp = await apiClient.post('/chaos/reset')
        this.status.tax_crash_active = false
        this.status.db_lock_active = false
        toast.success(resp.data.message)
        await this.fetchMetrics()
      } catch (e) {
        toast.error('Failed to reset chaos.')
      } finally {
        this.loading = false
      }
    },
  },
})
