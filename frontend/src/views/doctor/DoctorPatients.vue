<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">My Patients</h1>
      <p class="page-subtitle">All patients who have visited or are scheduled</p>
    </div>

    <!-- Search -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-12 col-md-6">
            <label class="form-label">Search Patients</label>
            <div class="input-icon-wrap">
              <i class="bi bi-search"></i>
              <input v-model="search" type="text" class="form-control" placeholder="Search by name or email..." @input="debouncedSearch" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div v-if="loading" class="empty-state">
      <div class="spinner-ring mx-auto"></div>
    </div>
    <div v-else-if="!patients.length" class="empty-state">
      <i class="bi bi-people"></i>
      <p>No patients found</p>
    </div>
    <div v-else class="patients-grid">
      <div v-for="p in patients" :key="p.id" class="patient-card">
        <div class="patient-card-header">
          <div class="avatar avatar-lg">{{ initials(p) }}</div>
          <div>
            <h4>{{ p.full_name }}</h4>
            <span class="role-pill">Patient</span>
          </div>
        </div>
        <div class="patient-info">
          <div class="info-row"><i class="bi bi-envelope"></i> {{ p.email }}</div>
          <div v-if="p.phone" class="info-row"><i class="bi bi-telephone"></i> {{ p.phone }}</div>
          <div v-if="p.patient_profile?.date_of_birth" class="info-row">
            <i class="bi bi-calendar3"></i> DOB: {{ p.patient_profile.date_of_birth }}
          </div>
          <div v-if="p.patient_profile?.blood_type" class="info-row">
            <i class="bi bi-droplet"></i> Blood Type: {{ p.patient_profile.blood_type }}
          </div>
        </div>
        <div class="patient-card-footer">
          <router-link :to="`/doctor/patients/${p.id}`" class="btn btn-primary btn-sm w-100">
            <i class="bi bi-folder2-open me-1"></i> View Records
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const patients = ref([])
const loading = ref(true)
const search = ref('')

const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'

async function loadPatients() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    const { data } = await api.get('/patients/', { params })
    patients.value = data.results || data
  } finally { loading.value = false }
}

let t = null
function debouncedSearch() {
  clearTimeout(t)
  t = setTimeout(loadPatients, 350)
}

onMounted(loadPatients)
</script>

<style scoped>
.patients-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.patient-card { background: white; border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden; transition: var(--transition); }
.patient-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.patient-card-header { display: flex; align-items: center; gap: 14px; padding: 20px; background: #f8faff; border-bottom: 1px solid var(--border); }
.patient-card-header h4 { font-size: 0.95rem; font-weight: 700; margin: 0 0 4px; }
.role-pill { background: var(--primary-light); color: var(--primary); padding: 2px 8px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.patient-info { padding: 16px 20px; display: flex; flex-direction: column; gap: 6px; }
.info-row { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--text-secondary); }
.info-row i { color: var(--primary); font-size: 0.85rem; width: 14px; }
.patient-card-footer { padding: 12px 20px; border-top: 1px solid var(--border); }
.input-icon-wrap { position: relative; }
.input-icon-wrap i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-icon-wrap .form-control { padding-left: 36px; }
</style>
