import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),
  actions: {
    show(message, type = 'info', duration = 4000) {
      const id = Date.now() + Math.random()
      this.toasts.push({ id, message, type })
      setTimeout(() => {
        this.remove(id)
      }, duration)
    },
    success(msg) {
      this.show(msg, 'success')
    },
    error(msg) {
      this.show(msg, 'error', 5000)
    },
    warning(msg) {
      this.show(msg, 'warning', 4500)
    },
    info(msg) {
      this.show(msg, 'info')
    },
    remove(id) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
  },
})
