<template>
  <div class="auth-wrapper">
    <div class="auth-left">
      <div class="auth-left-inner">
        <router-link to="/" class="back-link"><i class="bi bi-arrow-left"></i> Back to Home</router-link>
        <div class="auth-brand">
          <div class="brand-icon-lg"><i class="bi bi-hospital"></i></div>
          <h1>DentalCare</h1>
          <p>Professional Appointment Management</p>
        </div>
        <div class="auth-illustration">
          <div class="il-card">
            <i class="bi bi-calendar2-check"></i>
            <span>Appointment scheduled</span>
          </div>
          <div class="il-card il-card-2">
            <i class="bi bi-file-medical"></i>
            <span>Prescription ready</span>
          </div>
          <div class="il-card il-card-3">
            <i class="bi bi-shield-check"></i>
            <span>Secure & private</span>
          </div>
        </div>
      </div>
    </div>

    <div class="auth-right">
      <div class="auth-form-wrapper">
        <div class="auth-form-header">
          <h2>Welcome back</h2>
          <p>Sign in to your DentalCare account</p>
        </div>

        <!-- Role selector -->
        <div class="role-selector">
          <button
            v-for="r in roleOptions"
            :key="r.value"
            class="role-btn"
            :class="{ active: selectedRole === r.value }"
            @click="selectedRole = r.value"
          >
            <i :class="r.icon"></i>
            {{ r.label }}
          </button>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Email Address</label>
            <div class="input-icon-wrap">
              <i class="bi bi-envelope"></i>
              <input
                v-model="form.email"
                type="email"
                class="form-control"
                placeholder="you@example.com"
                required
                autocomplete="email"
              />
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label">Password</label>
            <div class="input-icon-wrap">
              <i class="bi bi-lock"></i>
              <input
                v-model="form.password"
                :type="showPass ? 'text' : 'password'"
                class="form-control"
                placeholder="••••••••"
                required
                autocomplete="current-password"
              />
              <button type="button" class="toggle-pass" @click="showPass = !showPass">
                <i :class="showPass ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
          </div>

          <div v-if="error" class="alert-error">
            <i class="bi bi-exclamation-circle"></i> {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-100 btn-submit" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-box-arrow-in-right me-1"></i>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="auth-divider"><span>Don't have an account?</span></div>
        <router-link to="/register" class="btn btn-outline-primary w-100">
          Create an account
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

const form = ref({ email: '', password: '' })
const selectedRole = ref('patient')
const showPass = ref(false)
const loading = ref(false)
const error = ref('')

const roleOptions = [
  { value: 'doctor', label: 'Doctor', icon: 'bi bi-person-badge' },
  { value: 'secretary', label: 'Secretary', icon: 'bi bi-person-workspace' },
  { value: 'patient', label: 'Patient', icon: 'bi bi-person-heart' },
]

async function handleLogin() {
  loading.value = true
  error.value = ''
  const result = await auth.login(form.value.email, form.value.password)
  loading.value = false

  if (result.success) {
    toast.success(`Welcome back, ${auth.fullName}!`)
    const redirect = route.query.redirect
    if (redirect) return router.push(redirect)
    router.push(`/${result.role}`)
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
}

/* Left Panel */
.auth-left {
  width: 420px;
  flex-shrink: 0;
  background: linear-gradient(160deg, #0d1b2e 0%, #1a3a5c 50%, #1a6fc4 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
  overflow: hidden;
}
.auth-left::after {
  content: '';
  position: absolute;
  bottom: -100px; right: -100px;
  width: 300px; height: 300px;
  background: rgba(6,214,160,0.15);
  border-radius: 50%;
  filter: blur(60px);
}
.auth-left-inner { width: 100%; position: relative; z-index: 1; }

.back-link {
  display: inline-flex; align-items: center; gap: 6px;
  color: rgba(255,255,255,0.6); text-decoration: none;
  font-size: 0.85rem; font-weight: 500;
  margin-bottom: 48px;
  transition: color 0.2s;
}
.back-link:hover { color: white; }

.auth-brand { margin-bottom: 48px; }
.brand-icon-lg {
  width: 60px; height: 60px;
  background: rgba(255,255,255,0.15);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; color: white;
  margin-bottom: 20px;
  border: 1px solid rgba(255,255,255,0.2);
  backdrop-filter: blur(10px);
}
.auth-brand h1 { color: white; font-size: 2rem; font-weight: 800; margin-bottom: 6px; }
.auth-brand p { color: rgba(255,255,255,0.6); font-size: 0.9rem; }

.auth-illustration { display: flex; flex-direction: column; gap: 12px; }
.il-card {
  display: flex; align-items: center; gap: 12px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 14px 18px;
  color: white;
  font-size: 0.88rem; font-weight: 500;
  animation: il-enter 0.5s ease both;
}
.il-card-2 { animation-delay: 0.1s; }
.il-card-3 { animation-delay: 0.2s; }
@keyframes il-enter {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}
.il-card i { font-size: 1.2rem; color: #5bc4ff; }

/* Right Panel */
.auth-right {
  flex: 1;
  display: flex; align-items: center; justify-content: center;
  background: #f8faff;
  padding: 40px;
}
.auth-form-wrapper { width: 100%; max-width: 440px; }

.auth-form-header { margin-bottom: 32px; }
.auth-form-header h2 { font-size: 1.75rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.auth-form-header p { color: #64748b; font-size: 0.95rem; }

/* Role Selector */
.role-selector {
  display: flex; gap: 8px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 28px;
}
.role-btn {
  flex: 1;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  padding: 8px;
  border: none;
  border-radius: 7px;
  font-size: 0.82rem;
  font-weight: 600;
  font-family: var(--font-sans);
  color: #64748b;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}
.role-btn.active {
  background: var(--primary);
  color: white;
  box-shadow: 0 2px 8px rgba(26,111,196,0.3);
}
.role-btn:not(.active):hover { background: #f1f5f9; }

/* Input */
.input-icon-wrap { position: relative; }
.input-icon-wrap i:first-child {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  color: #94a3b8; font-size: 0.95rem;
}
.input-icon-wrap .form-control { padding-left: 40px; }
.toggle-pass {
  position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
  background: none; border: none; color: #94a3b8; cursor: pointer; padding: 4px;
}
.toggle-pass:hover { color: var(--primary); }

.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.88rem;
  margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}

.btn-submit { padding: 12px; font-size: 0.95rem; }

.auth-divider {
  text-align: center; position: relative; margin: 20px 0;
  color: #94a3b8; font-size: 0.85rem;
}
.auth-divider::before, .auth-divider::after {
  content: '';
  position: absolute; top: 50%;
  width: calc(50% - 80px); height: 1px;
  background: #e2e8f0;
}
.auth-divider::before { left: 0; }
.auth-divider::after { right: 0; }

@media (max-width: 768px) {
  .auth-left { display: none; }
  .auth-right { padding: 32px 24px; }
}
</style>
