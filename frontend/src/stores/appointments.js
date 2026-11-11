import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAppointmentStore = defineStore('appointments', {
  state: () => ({
    appointments: [],
    currentAppointment: null,
    statistics: null,
    loading: false,
    error: null,
    pagination: { count: 0, next: null, previous: null },
  }),

  actions: {
    async fetchAppointments(params = {}) {
      this.loading = true
      try {
        const { data } = await api.get('/appointments/', { params })
        this.appointments = data.results || data
        if (data.count !== undefined) {
          this.pagination = { count: data.count, next: data.next, previous: data.previous }
        }
        return data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to load appointments.'
      } finally {
        this.loading = false
      }
    },

    async fetchAppointment(id) {
      this.loading = true
      try {
        const { data } = await api.get(`/appointments/${id}/`)
        this.currentAppointment = data
        return data
      } catch (err) {
        this.error = 'Failed to load appointment.'
      } finally {
        this.loading = false
      }
    },

    async createAppointment(payload) {
      this.loading = true
      try {
        const { data } = await api.post('/appointments/', payload)
        this.appointments.unshift(data)
        return { success: true, data }
      } catch (err) {
        const errors = err.response?.data
        const msg = typeof errors === 'object'
          ? Object.values(errors).flat().join(' ')
          : 'Failed to create appointment.'
        return { success: false, error: msg }
      } finally {
        this.loading = false
      }
    },

    async updateAppointment(id, payload) {
      this.loading = true
      try {
        const { data } = await api.patch(`/appointments/${id}/`, payload)
        const idx = this.appointments.findIndex(a => a.id === id)
        if (idx !== -1) this.appointments[idx] = data
        return { success: true, data }
      } catch (err) {
        return { success: false, error: 'Failed to update appointment.' }
      } finally {
        this.loading = false
      }
    },

    async updateStatus(id, newStatus) {
      try {
        const { data } = await api.patch(`/appointments/${id}/update_status/`, { status: newStatus })
        const idx = this.appointments.findIndex(a => a.id === id)
        if (idx !== -1) this.appointments[idx] = data
        return { success: true, data }
      } catch (err) {
        return { success: false, error: 'Failed to update status.' }
      }
    },

    async deleteAppointment(id) {
      try {
        await api.delete(`/appointments/${id}/`)
        this.appointments = this.appointments.filter(a => a.id !== id)
        return { success: true }
      } catch (err) {
        return { success: false, error: 'Failed to delete appointment.' }
      }
    },

    async fetchStatistics() {
      try {
        const { data } = await api.get('/appointments/statistics/')
        this.statistics = data
        return data
      } catch (err) {
        return null
      }
    }
  }
})
