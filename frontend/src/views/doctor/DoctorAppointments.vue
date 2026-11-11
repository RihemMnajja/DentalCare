<template>
  <div>
    <div class="page-header d-flex justify-content-between align-items-start flex-wrap gap-3">
      <div>
        <h1 class="page-title">Appointments</h1>
        <p class="page-subtitle">Manage and review your patient appointments</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-12 col-md-3">
            <label class="form-label">Filter by Date</label>
            <input v-model="filters.date" type="date" class="form-control" @change="loadAppointments" />
          </div>
          <div class="col-12 col-md-3">
            <label class="form-label">Status</label>
            <select v-model="filters.status" class="form-select" @change="loadAppointments">
              <option value="">All Statuses</option>
              <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </div>
          <div class="col-12 col-md-4">
            <label class="form-label">Search Patient</label>
            <div class="input-icon-wrap">
              <i class="bi bi-search"></i>
              <input v-model="filters.search" type="text" class="form-control" placeholder="Search by name..." @input="debouncedSearch" />
            </div>
          </div>
          <div class="col-12 col-md-2 d-flex align-items-end">
            <button class="btn btn-outline-primary w-100" @click="clearFilters">
              <i class="bi bi-x-circle"></i> Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card">
      <div class="card-header">
        <span>
          <i class="bi bi-list-ul me-2 text-primary"></i>
          Appointments
          <span class="count-badge ms-2">{{ appointments.length }}</span>
        </span>
      </div>
      <div class="card-body p-0">
        <div v-if="loading" class="empty-state">
          <div class="spinner-ring mx-auto"></div>
        </div>
        <div v-else-if="!appointments.length" class="empty-state">
          <i class="bi bi-calendar-x"></i>
          <p>No appointments found</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table mb-0">
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Patient</th>
                <th>Treatment</th>
                <th>Duration</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in appointments" :key="apt.id">
                <td>
                  <div class="datetime-cell">
                    <span class="date">{{ formatDate(apt.date) }}</span>
                    <span class="time">{{ apt.time?.slice(0,5) }}</span>
                  </div>
                </td>
                <td>
                  <div class="d-flex align-items-center gap-2">
                    <div class="avatar">{{ initials(apt.patient_detail) }}</div>
                    <div>
                      <div class="fw-600">{{ apt.patient_detail?.full_name }}</div>
                      <small class="text-muted">{{ apt.patient_detail?.email }}</small>
                    </div>
                  </div>
                </td>
                <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
                <td>{{ apt.duration_minutes }} min</td>
                <td>
                  <select :value="apt.status" class="status-select" @change="e => updateStatus(apt.id, e.target.value)">
                    <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
                  </select>
                </td>
                <td>
                  <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-outline-primary" @click="openNoteModal(apt)">
                      <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-success" @click="openPrescriptionModal(apt)">
                      <i class="bi bi-file-medical"></i>
                    </button>
                    <router-link :to="`/doctor/patients/${apt.patient}`" class="btn btn-sm btn-outline-secondary">
                      <i class="bi bi-person"></i>
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Note Modal -->
    <div v-if="noteModal.open" class="modal-overlay" @click.self="noteModal.open = false">
      <div class="modal-box">
        <div class="modal-box-header">
          <h3><i class="bi bi-pencil-square me-2"></i>Add Medical Note</h3>
          <button @click="noteModal.open = false" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-box-body">
          <div class="mb-3">
            <label class="form-label">Patient</label>
            <input type="text" class="form-control" :value="noteModal.apt?.patient_detail?.full_name" readonly />
          </div>
          <div class="mb-3">
            <label class="form-label">Note Type</label>
            <select v-model="noteForm.note_type" class="form-select">
              <option value="diagnosis">Diagnosis</option>
              <option value="advice">Advice</option>
              <option value="observation">Observation</option>
              <option value="follow_up">Follow-up</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Title</label>
            <input v-model="noteForm.title" type="text" class="form-control" placeholder="Note title" />
          </div>
          <div class="mb-3">
            <label class="form-label">Content</label>
            <textarea v-model="noteForm.content" class="form-control" rows="4" placeholder="Write your note here..."></textarea>
          </div>
          <div class="form-check">
            <input v-model="noteForm.is_private" class="form-check-input" type="checkbox" id="privateNote" />
            <label class="form-check-label" for="privateNote">Private note (not visible to patient)</label>
          </div>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-outline-secondary" @click="noteModal.open = false">Cancel</button>
          <button class="btn btn-primary" @click="saveNote" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            Save Note
          </button>
        </div>
      </div>
    </div>

    <!-- Prescription Modal -->
    <div v-if="rxModal.open" class="modal-overlay" @click.self="rxModal.open = false">
      <div class="modal-box">
        <div class="modal-box-header">
          <h3><i class="bi bi-file-medical me-2"></i>New Prescription</h3>
          <button @click="rxModal.open = false" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-box-body">
          <div class="mb-3">
            <label class="form-label">Patient</label>
            <input type="text" class="form-control" :value="rxModal.apt?.patient_detail?.full_name" readonly />
          </div>
          <div class="mb-3">
            <label class="form-label">Medication</label>
            <input v-model="rxForm.medication_name" type="text" class="form-control" placeholder="e.g. Amoxicillin 500mg" />
          </div>
          <div class="row g-3 mb-3">
            <div class="col-6">
              <label class="form-label">Dosage</label>
              <input v-model="rxForm.dosage" type="text" class="form-control" placeholder="e.g. 500mg" />
            </div>
            <div class="col-6">
              <label class="form-label">Frequency</label>
              <input v-model="rxForm.frequency" type="text" class="form-control" placeholder="e.g. 3x daily" />
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Duration</label>
            <input v-model="rxForm.duration" type="text" class="form-control" placeholder="e.g. 7 days" />
          </div>
          <div class="mb-3">
            <label class="form-label">Instructions</label>
            <textarea v-model="rxForm.instructions" class="form-control" rows="3" placeholder="Special instructions..."></textarea>
          </div>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-outline-secondary" @click="rxModal.open = false">Cancel</button>
          <button class="btn btn-primary" @click="savePrescription" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            Issue Prescription
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'
import { format, parseISO } from 'date-fns'

const toast = useToast()
const appointments = ref([])
const loading = ref(true)
const saving = ref(false)

const filters = ref({ date: '', status: '', search: '' })

const statuses = [
  { value: 'pending', label: 'Pending' },
  { value: 'confirmed', label: 'Confirmed' },
  { value: 'completed', label: 'Completed' },
  { value: 'cancelled', label: 'Cancelled' },
  { value: 'no_show', label: 'No Show' },
]

const noteModal = ref({ open: false, apt: null })
const rxModal = ref({ open: false, apt: null })

const noteForm = ref({ note_type: 'observation', title: '', content: '', is_private: false })
const rxForm = ref({ medication_name: '', dosage: '', frequency: '', duration: '', instructions: '' })

const treatments = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatmentLabel = t => treatments[t] || t
const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
const formatDate = d => { try { return format(parseISO(d), 'MMM d, yyyy') } catch { return d } }

async function loadAppointments() {
  loading.value = true
  const params = {}
  if (filters.value.date) params.date = filters.value.date
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.search) params.search = filters.value.search
  try {
    const { data } = await api.get('/appointments/', { params })
    appointments.value = data.results || data
  } finally { loading.value = false }
}

let searchTimer = null
function debouncedSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(loadAppointments, 400)
}

function clearFilters() {
  filters.value = { date: '', status: '', search: '' }
  loadAppointments()
}

async function updateStatus(id, status) {
  const result = await api.patch(`/appointments/${id}/update_status/`, { status })
  const apt = appointments.value.find(a => a.id === id)
  if (apt) apt.status = status
  toast.success('Status updated')
}

function openNoteModal(apt) {
  noteModal.value = { open: true, apt }
  noteForm.value = { note_type: 'observation', title: '', content: '', is_private: false }
}

function openPrescriptionModal(apt) {
  rxModal.value = { open: true, apt }
  rxForm.value = { medication_name: '', dosage: '', frequency: '', duration: '', instructions: '' }
}

async function saveNote() {
  saving.value = true
  try {
    await api.post('/notes/', {
      ...noteForm.value,
      patient: noteModal.value.apt.patient,
      appointment: noteModal.value.apt.id,
    })
    toast.success('Medical note saved!')
    noteModal.value.open = false
  } catch {
    toast.error('Failed to save note.')
  } finally { saving.value = false }
}

async function savePrescription() {
  saving.value = true
  try {
    await api.post('/prescriptions/', {
      ...rxForm.value,
      patient: rxModal.value.apt.patient,
      appointment: rxModal.value.apt.id,
    })
    toast.success('Prescription issued!')
    rxModal.value.open = false
  } catch {
    toast.error('Failed to issue prescription.')
  } finally { saving.value = false }
}

onMounted(loadAppointments)
</script>

<style scoped>
.count-badge { background: var(--primary-light); color: var(--primary); padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
.datetime-cell { display: flex; flex-direction: column; }
.date { font-weight: 600; font-size: 0.88rem; }
.time { font-size: 0.78rem; color: var(--text-muted); }
.treatment-tag { background: #f1f5f9; color: #475569; padding: 3px 9px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; }
.fw-600 { font-weight: 600; font-size: 0.88rem; }
.status-select { border: 1px solid var(--border); border-radius: 6px; padding: 5px 8px; font-size: 0.8rem; font-family: var(--font-sans); font-weight: 600; cursor: pointer; background: white; }
.input-icon-wrap { position: relative; }
.input-icon-wrap i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-icon-wrap .form-control { padding-left: 36px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 500; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal-box { background: white; border-radius: var(--radius-lg); width: 100%; max-width: 520px; box-shadow: var(--shadow-lg); }
.modal-box-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border); }
.modal-box-header h3 { font-size: 1.05rem; font-weight: 700; margin: 0; }
.close-btn { background: none; border: none; font-size: 1rem; cursor: pointer; color: var(--text-muted); padding: 4px; }
.close-btn:hover { color: var(--danger); }
.modal-box-body { padding: 24px; max-height: 60vh; overflow-y: auto; }
.modal-box-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 24px; border-top: 1px solid var(--border); }
</style>
