import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useCityStore = defineStore('city', {
  state: () => ({
    selectedCity: localStorage.getItem('ticketlocal_city') || 'Hyderabad',
    cities: [
      { id: 1, name: 'Hyderabad' },
      { id: 2, name: 'Bangalore' },
      { id: 3, name: 'Mumbai' },
    ],
    isCityModalOpen: false,
  }),
  actions: {
    async fetchCities() {
      try {
        const resp = await apiClient.get('/cities')
        if (resp.data && resp.data.length > 0) {
          this.cities = resp.data
        }
      } catch (e) {
        // Fallback default cities
      }
    },
    setCity(cityName) {
      this.selectedCity = cityName
      localStorage.setItem('ticketlocal_city', cityName)
      this.isCityModalOpen = false
    },
    openCityModal() {
      this.isCityModalOpen = true
    },
    closeCityModal() {
      this.isCityModalOpen = false
    },
  },
})
