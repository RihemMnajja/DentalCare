<template>
  <div class="auth-wrapper">
    <div class="auth-left">
      <div class="auth-left-inner">
        <router-link to="/" class="back-link"><i class="bi bi-arrow-left"></i> Back to Home</router-link>
        <div class="auth-brand">
          <div class="brand-icon-lg"><i class="bi bi-hospital"></i></div>
          <h1>Join DentalCare</h1>
          <p>Create your account in seconds</p>
        </div>
        <div class="steps-guide">
          <div v-for="(step, i) in steps" :key="i" class="step" :class="{ done: currentStep > i + 1, active: currentStep === i + 1 }">
            <div class="step-num">{{ i + 1 }}</div>
            <div>
              <strong>{{ step.title }}</strong>
              <span>{{ step.desc }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="auth-right">
      <div class="auth-form-wrapper">
        <div class="auth-form-header">
          <h2>Create Account</h2>
          <p>Fill in your details to get started</p>
        </div>

        <form @submit.prevent="handleRegister">
          <!-- Role -->
          <div class="mb-3">
            <label class="form-label">I am a</label>
            <div class="role-selector">
              <button v-for="r in roleOptions" :key="r.value" type="button"
                class="role-btn" :class="{ active: form.role === r.value }"
                @click="form.role = r.value">
                <i :class="r.icon"></i> {{ r.label }}
              </button>
            </div>
          </div>

          <!-- Name row -->
          <div class="row g-3 mb-3">
            <div class="col-6">
              <label class="form-label">First Name</label>
              <input v-model="form.first_name" type="text" class="form-control" placeholder="Jane" required />
            </div>
            <div class="col-6">
              <label class="form-label">Last Name</label>
              <input v-model="form.last_name" type="text" class="form-control" placeholder="Doe" required />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <div class="input-icon-wrap">
              <i class="bi bi-envelope"></i>
              <input v-model="form.email" type="email" class="form-control" placeholder="you@example.com" required />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Phone (optional)</label>
            <div class="input-icon-wrap">
              <i class="bi bi-telephone"></i>
              <input v-model="form.phone" type="tel" class="form-control" placeholder="+1 234 567 890" />
            </div>
          </div>

          <div class="row g-3 mb-4">
            <div class="col-6">
              <label class="form-label">Password</label>
              <div class="input-icon-wrap">
                <i class="bi bi-lock"></i>
                <input v-model="form.password" :type="showPass ? 'text' : 'password'" class="form-control" placeholder="••••••••" required autocomplete="new-password" />
                <button type="button" class="toggle-pass" @click="showPass = !showPass">
                  <i :class="showPass ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>
            <div class="col-6">
              <label class="form-label">Confirm Password</label>
              <div class="input-icon-wrap">
                <i class="bi bi-lock-fill"></i>
                <input v-model="form.password2" :type="showPass ? 'text' : 'password'" class="form-control" placeholder="••••••••" required />
              </div>
            </div>
          </div>

          <!-- Doctor extra fields -->
          <div v-if="form.role === 'doctor'" class="extra-fields">
            <div class="extra-header"><i class="bi bi-person-badge"></i> Doctor Information</div>
            <div class="mb-3">
              <label class="form-label">Specialization</label>
              <input v-model="form.doctor_profile.specialization" type="text" class="form-control" placeholder="e.g. Orthodontics" />
            </div>
            <div class="mb-3">
              <label class="form-label">License Number</label>
              <input v-model="form.doctor_profile.license_number" type="text" class="form-control" placeholder="DR-12345" />
            </div>
          </div>

          <!-- Patient extra fields -->
          <div v-if="form.role === 'patient'" class="extra-fields">
            <div class="extra-header"><i class="bi bi-person-heart"></i> Patient Information</div>
            <div class="row g-3 mb-3">
              <div class="col-6">
                <label class="form-label">Date of Birth</label>
                <input v-model="form.patient_profile.date_of_birth" type="date" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">Gender</label>
                <select v-model="form.patient_profile.gender" class="form-select">
                  <option value="">Select</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>
              </div>
            </div>
          </div>

          <div v-if="error" class="alert-error">
            <i class="bi bi-exclamation-circle"></i> {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-100 btn-submit" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-person-plus me-1"></i>
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>
        </form>

        <div class="auth-divider"><span>Already have an account?</span></div>
        <router-link to="/login" class="btn btn-outline-primary w-100">Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

const showPass = ref(false)
const loading = ref(false)
const error = ref('')
const currentStep = ref(1)

const form = ref({
  role: route.query.role || 'patient',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  password: '',
  password2: '',
  doctor_profile: { specialization: 'General Dentistry', license_number: '' },
  patient_profile: { date_of_birth: '', gender: '' },
})

const roleOptions = [
  { value: 'doctor', label: 'Doctor', icon: 'bi bi-person-badge' },
  { value: 'secretary', label: 'Secretary', icon: 'bi bi-person-workspace' },
  { value: 'patient', label: 'Patient', icon: 'bi bi-person-heart' },
]

const steps = [
  { title: 'Choose Role', desc: 'Doctor, secretary or patient' },
  { title: 'Your Details', desc: 'Name, email, password' },
  { title: 'Done!', desc: 'Access your dashboard' },
]

async function handleRegister() {
  if (form.value.password !== form.value.password2) {
    error.value = 'Passwords do not match.'
    return
  }
  loading.value = true
  error.value = ''

  const payload = { ...form.value }
  if (payload.role !== 'doctor') delete payload.doctor_profile
  if (payload.role !== 'patient') delete payload.patient_profile

  const result = await auth.register(payload)
  loading.value = false

  if (result.success) {
    toast.success('Account created successfully! Welcome aboard.')
    router.push(`/${result.role}`)
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.auth-wrapper { min-height: 100vh; display: flex; }

.auth-left {
  width: 420px; flex-shrink: 0;
  background: linear-gradient(160deg, #0d1b2e 0%, #1a3a5c 50%, #1a6fc4 100%);
  display: flex; align-items: flex-start; justify-content: center;
  padding: 40px; overflow-y: auto;
}
.auth-left-inner { width: 100%; }

.back-link { display: inline-flex; align-items: center; gap: 6px; color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.85rem; font-weight: 500; margin-bottom: 48px; transition: color 0.2s; }
.back-link:hover { color: white; }

.auth-brand { margin-bottom: 40px; }
.brand-icon-lg { width: 60px; height: 60px; background: rgba(255,255,255,0.15); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; color: white; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.2); }
.auth-brand h1 { color: white; font-size: 1.75rem; font-weight: 800; margin-bottom: 6px; }
.auth-brand p { color: rgba(255,255,255,0.6); font-size: 0.9rem; }

.steps-guide { display: flex; flex-direction: column; gap: 16px; }
.step { display: flex; align-items: center; gap: 14px; }
.step-num {
  width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 0.85rem;
  border: 2px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.5);
  transition: all 0.3s;
}
.step.active .step-num { background: white; color: var(--primary); border-color: white; }
.step.done .step-num { background: #06d6a0; border-color: #06d6a0; color: white; }
.step div { display: flex; flex-direction: column; }
.step strong { font-size: 0.88rem; color: rgba(255,255,255,0.9); }
.step span { font-size: 0.78rem; color: rgba(255,255,255,0.5); }

.auth-right { flex: 1; display: flex; align-items: flex-start; justify-content: center; background: #f8faff; padding: 48px 40px; overflow-y: auto; }
.auth-form-wrapper { width: 100%; max-width: 500px; }
.auth-form-header { margin-bottom: 28px; }
.auth-form-header h2 { font-size: 1.75rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.auth-form-header p { color: #64748b; }

.role-selector { display: flex; gap: 8px; background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 4px; }
.role-btn { flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 9px; border: none; border-radius: 7px; font-size: 0.82rem; font-weight: 600; font-family: var(--font-sans); color: #64748b; background: transparent; cursor: pointer; transition: all 0.2s; }
.role-btn.active { background: var(--primary); color: white; box-shadow: 0 2px 8px rgba(26,111,196,0.3); }
.role-btn:not(.active):hover { background: #f1f5f9; }

.input-icon-wrap { position: relative; }
.input-icon-wrap > i:first-child { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 0.95rem; }
.input-icon-wrap .form-control { padding-left: 40px; }
.toggle-pass { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; color: #94a3b8; cursor: pointer; padding: 4px; }
.toggle-pass:hover { color: var(--primary); }

.extra-fields { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 20px; }
.extra-header { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 0.88rem; color: var(--primary); margin-bottom: 14px; }

.alert-error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; border-radius: 8px; padding: 10px 14px; font-size: 0.88rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.btn-submit { padding: 12px; font-size: 0.95rem; }
.auth-divider { text-align: center; position: relative; margin: 20px 0; color: #94a3b8; font-size: 0.85rem; }
.auth-divider::before, .auth-divider::after { content: ''; position: absolute; top: 50%; width: calc(50% - 90px); height: 1px; background: #e2e8f0; }
.auth-divider::before { left: 0; }
.auth-divider::after { right: 0; }

@media (max-width: 768px) { .auth-left { display: none; } .auth-right { padding: 32px 20px; } }
</style>
