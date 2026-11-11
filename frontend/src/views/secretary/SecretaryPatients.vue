<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Patients</h1>
      <p class="page-subtitle">All registered patients in the system</p>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="input-icon-wrap" style="max-width:400px">
          <i class="bi bi-search"></i>
          <input v-model="search" type="text" class="form-control" placeholder="Search by name, email..." @input="debouncedSearch" />
        </div>
      </div>
    </div>

    <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
    <div v-else-if="!patients.length" class="empty-state card"><i class="bi bi-people"></i><p>No patients found</p></div>
    <div v-else class="card">
      <div class="card-body p-0">
        <table class="table mb-0">
          <thead><tr><th>Patient</th><th>Email</th><th>Phone</th><th>Blood Type</th><th>Gender</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="p in patients" :key="p.id">
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="avatar">{{ initials(p) }}</div>
                  <span class="fw-600">{{ p.full_name }}</span>
                </div>
              </td>
              <td>{{ p.email }}</td>
              <td>{{ p.phone || '—' }}</td>
              <td>{{ p.patient_profile?.blood_type || '—' }}</td>
              <td>{{ genderLabel(p.patient_profile?.gender) }}</td>
              <td>
                <button class="btn btn-sm btn-outline-primary" @click="viewPatient(p)">
                  <i class="bi bi-eye"></i> View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Patient Detail Modal -->
    <div v-if="viewModal" class="modal-overlay" @click.self="viewModal = false">
      <div class="modal-box modal-lg">
        <div class="modal-box-header">
          <h3><i class="bi bi-person me-2"></i>Patient Details</h3>
          <button @click="viewModal = false" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-box-body" v-if="selectedPatient">
          <div class="patient-detail-header">
            <div class="avatar avatar-lg">{{ initials(selectedPatient) }}</div>
            <div>
              <h4>{{ selectedPatient.full_name }}</h4>
              <p>{{ selectedPatient.email }}</p>
            </div>
          </div>
          <div class="row g-3 mt-2">
            <div class="col-6"><div class="detail-item"><span>Phone</span><strong>{{ selectedPatient.phone || '—' }}</strong></div></div>
            <div class="col-6"><div class="detail-item"><span>Blood Type</span><strong>{{ selectedPatient.patient_profile?.blood_type || '—' }}</strong></div></div>
            <div class="col-6"><div class="detail-item"><span>Date of Birth</span><strong>{{ selectedPatient.patient_profile?.date_of_birth || '—' }}</strong></div></div>
            <div class="col-6"><div class="detail-item"><span>Gender</span><strong>{{ genderLabel(selectedPatient.patient_profile?.gender) }}</strong></div></div>
            <div class="col-12"><div class="detail-item"><span>Address</span><strong>{{ selectedPatient.patient_profile?.address || '—' }}</strong></div></div>
            <div class="col-6"><div class="detail-item"><span>Emergency Contact</span><strong>{{ selectedPatient.patient_profile?.emergency_contact || '—' }}</strong></div></div>
            <div class="col-6"><div class="detail-item"><span>Insurance #</span><strong>{{ selectedPatient.patient_profile?.insurance_number || '—' }}</strong></div></div>
          </div>
          <div v-if="selectedPatient.patient_profile?.allergies" class="mt-3">
            <div class="alert-info-box"><i class="bi bi-exclamation-triangle"></i> <strong>Allergies:</strong> {{ selectedPatient.patient_profile.allergies }}</div>
          </div>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-outline-secondary" @click="viewModal = false">Close</button>
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
const viewModal = ref(false)
const selectedPatient = ref(null)

const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
const genderLabel = g => ({ M: 'Male', F: 'Female', O: 'Other' }[g] || '—')

async function load() {
  loading.value = true
  const params = {}
  if (search.value) params.search = search.value
  try {
    const { data } = await api.get('/patients/', { params })
    patients.value = data.results || data
  } finally { loading.value = false }
}

let t = null
function debouncedSearch() { clearTimeout(t); t = setTimeout(load, 350) }
function viewPatient(p) { selectedPatient.value = p; viewModal.value = true }

onMounted(load)
</script>

<style scoped>
.fw-600 { font-weight: 600; font-size: 0.88rem; }
.input-icon-wrap { position: relative; }
.input-icon-wrap i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-icon-wrap .form-control { padding-left: 36px; }
.patient-detail-header { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }
.patient-detail-header h4 { margin: 0 0 4px; font-size: 1.1rem; }
.patient-detail-header p { margin: 0; color: var(--text-muted); font-size: 0.9rem; }
.detail-item { background: #f8faff; border-radius: 8px; padding: 10px 14px; }
.detail-item span { display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); font-weight: 700; margin-bottom: 4px; }
.detail-item strong { font-size: 0.9rem; }
.alert-info-box { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px 16px; font-size: 0.88rem; color: #92400e; display: flex; gap: 8px; align-items: flex-start; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 500; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal-box { background: white; border-radius: var(--radius-lg); width: 100%; max-width: 520px; box-shadow: var(--shadow-lg); }
.modal-lg { max-width: 620px; }
.modal-box-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border); }
.modal-box-header h3 { font-size: 1.05rem; font-weight: 700; margin: 0; }
.close-btn { background: none; border: none; font-size: 1rem; cursor: pointer; color: var(--text-muted); padding: 4px; }
.modal-box-body { padding: 24px; max-height: 60vh; overflow-y: auto; }
.modal-box-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 24px; border-top: 1px solid var(--border); }
</style>
