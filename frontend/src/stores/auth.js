import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
    isDoctor: (state) => state.user?.role === 'doctor',
    isSecretary: (state) => state.user?.role === 'secretary',
    isPatient: (state) => state.user?.role === 'patient',
    isAdmin: (state) => state.user?.role === 'admin',
    userRole: (state) => state.user?.role || null,
    fullName: (state) => state.user?.full_name || state.user?.email || '',
  },

  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.post('/auth/login/', { email, password })
        this._setAuth(data)
        return { success: true, role: data.user.role }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Invalid credentials.'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(payload) {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.post('/auth/register/', payload)
        this._setAuth(data)
        return { success: true, role: data.user.role }
      } catch (err) {
        const errors = err.response?.data
        this.error = typeof errors === 'object'
          ? Object.values(errors).flat().join(' ')
          : 'Registration failed.'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await api.post('/auth/logout/', { refresh: this.refreshToken })
        }
      } catch (_) {}
      this._clearAuth()
    },

    async fetchProfile() {
      try {
        const { data } = await api.get('/profile/')
        this.user = { ...this.user, ...data }
        localStorage.setItem('user', JSON.stringify(this.user))
        return data
      } catch (err) {
        return null
      }
    },

    _setAuth(data) {
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.user = data.user
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
    },

    _clearAuth() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  }
})
