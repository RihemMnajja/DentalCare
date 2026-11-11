<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">My Profile</h1>
      <p class="page-subtitle">View and update your personal information</p>
    </div>

    <div class="row g-4">
      <!-- Avatar & Basic Info -->
      <div class="col-12 col-lg-4">
        <div class="card text-center p-4">
          <div class="profile-avatar mx-auto">
            {{ initials }}
          </div>
          <h3 class="mt-3 mb-1">{{ auth.fullName }}</h3>
          <span class="role-pill">Patient</span>
          <div class="profile-contact mt-3">
            <div class="contact-item"><i class="bi bi-envelope"></i> {{ auth.user?.email }}</div>
            <div v-if="auth.user?.phone" class="contact-item"><i class="bi bi-telephone"></i> {{ auth.user?.phone }}</div>
            <div class="contact-item"><i class="bi bi-calendar3"></i> Joined {{ joinDate }}</div>
          </div>
        </div>
      </div>

      <!-- Edit Form -->
      <div class="col-12 col-lg-8">
        <div class="card mb-4">
          <div class="card-header">
            <span><i class="bi bi-person-gear me-2 text-primary"></i>Personal Information</span>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-6">
                <label class="form-label">First Name</label>
                <input v-model="form.first_name" type="text" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">Last Name</label>
                <input v-model="form.last_name" type="text" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Phone</label>
                <input v-model="form.phone" type="tel" class="form-control" />
              </div>
            </div>
          </div>
        </div>

        <!-- Health Info -->
        <div class="card mb-4">
          <div class="card-header">
            <span><i class="bi bi-heart-pulse me-2 text-primary"></i>Health Information</span>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Date of Birth</label>
                <input v-model="profile.date_of_birth" type="date" class="form-control" />
              </div>
              <div class="col-md-3">
                <label class="form-label">Gender</label>
                <select v-model="profile.gender" class="form-select">
                  <option value="">Select</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label">Blood Type</label>
                <select v-model="profile.blood_type" class="form-select">
                  <option value="">—</option>
                  <option v-for="bt in bloodTypes" :key="bt" :value="bt">{{ bt }}</option>
                </select>
              </div>
              <div class="col-12">
                <label class="form-label">Address</label>
                <textarea v-model="profile.address" class="form-control" rows="2"></textarea>
              </div>
              <div class="col-md-6">
                <label class="form-label">Emergency Contact</label>
                <input v-model="profile.emergency_contact" type="text" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Emergency Phone</label>
                <input v-model="profile.emergency_phone" type="tel" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Allergies</label>
                <textarea v-model="profile.allergies" class="form-control" rows="2" placeholder="List any known allergies..."></textarea>
              </div>
              <div class="col-12">
                <label class="form-label">Medical History</label>
                <textarea v-model="profile.medical_history" class="form-control" rows="3" placeholder="Previous conditions, surgeries..."></textarea>
              </div>
              <div class="col-md-6">
                <label class="form-label">Insurance Number</label>
                <input v-model="profile.insurance_number" type="text" class="form-control" />
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-end gap-3">
          <button class="btn btn-outline-secondary" @click="resetForm">
            <i class="bi bi-arrow-counterclockwise me-1"></i> Reset
          </button>
          <button class="btn btn-primary" @click="save" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            <i v-else class="bi bi-check2 me-1"></i>
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import api from '@/api/axios'
import { format, parseISO } from 'date-fns'

const auth = useAuthStore()
const toast = useToast()
const saving = ref(false)

const bloodTypes = ['A+','A-','B+','B-','AB+','AB-','O+','O-']

const initials = computed(() => {
  const u = auth.user
  return u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
})

const joinDate = computed(() => {
  try { return format(parseISO(auth.user?.date_joined), 'MMMM yyyy') } catch { return '' }
})

const form = ref({ first_name: '', last_name: '', phone: '' })
const profile = ref({ date_of_birth: '', gender: '', blood_type: '', address: '', emergency_contact: '', emergency_phone: '', allergies: '', medical_history: '', insurance_number: '' })

function resetForm() {
  const u = auth.user
  form.value = { first_name: u?.first_name || '', last_name: u?.last_name || '', phone: u?.phone || '' }
  const p = u?.patient_profile || {}
  profile.value = { date_of_birth: p.date_of_birth || '', gender: p.gender || '', blood_type: p.blood_type || '', address: p.address || '', emergency_contact: p.emergency_contact || '', emergency_phone: p.emergency_phone || '', allergies: p.allergies || '', medical_history: p.medical_history || '', insurance_number: p.insurance_number || '' }
}

async function save() {
  saving.value = true
  try {
    await api.patch('/profile/', { ...form.value })
    await auth.fetchProfile()
    toast.success('Profile updated successfully!')
  } catch { toast.error('Failed to update profile.') }
  finally { saving.value = false }
}

onMounted(async () => {
  await auth.fetchProfile()
  resetForm()
})
</script>

<style scoped>
.profile-avatar { width: 80px; height: 80px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 800; }
.role-pill { background: var(--primary-light); color: var(--primary); padding: 4px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
.profile-contact { display: flex; flex-direction: column; gap: 8px; text-align: left; }
.contact-item { display: flex; align-items: center; gap: 8px; font-size: 0.88rem; color: var(--text-secondary); }
.contact-item i { color: var(--primary); width: 16px; }
</style>
