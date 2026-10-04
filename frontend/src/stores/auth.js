import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('ticketlocal_user') || 'null'),
    token: localStorage.getItem('ticketlocal_token') || null,
    isAuthModalOpen: false,
    authModalMode: 'login', // 'login' or 'register'
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    openLogin() {
      this.authModalMode = 'login'
      this.isAuthModalOpen = true
    },
    openRegister() {
      this.authModalMode = 'register'
      this.isAuthModalOpen = true
    },
    closeAuthModal() {
      this.isAuthModalOpen = false
    },
    async login(email, password) {
      try {
        const response = await apiClient.post('/auth/login', { email, password })
        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('ticketlocal_token', this.token)
        localStorage.setItem('ticketlocal_user', JSON.stringify(this.user))
        this.closeAuthModal()
        return { success: true }
      } catch (err) {
        return {
          success: false,
          error: err.response?.data?.detail || 'Login failed. Please verify your credentials.',
        }
      }
    },
    async register(name, email, password) {
      try {
        const response = await apiClient.post('/auth/register', { name, email, password })
        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('ticketlocal_token', this.token)
        localStorage.setItem('ticketlocal_user', JSON.stringify(this.user))
        this.closeAuthModal()
        return { success: true }
      } catch (err) {
        return {
          success: false,
          error: err.response?.data?.detail || 'Registration failed. Please try again.',
        }
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('ticketlocal_token')
      localStorage.removeItem('ticketlocal_user')
    },
  },
})
