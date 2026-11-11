<template>
  <div>
    <div class="page-header d-flex justify-content-between align-items-center flex-wrap gap-3">
      <div>
        <h1 class="page-title">Appointments</h1>
        <p class="page-subtitle">Schedule, edit, and manage all appointments</p>
      </div>
      <button class="btn btn-primary" @click="openModal()">
        <i class="bi bi-plus-lg me-1"></i> New Appointment
      </button>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-12 col-md-2">
            <label class="form-label">Date From</label>
            <input v-model="filters.date_from" type="date" class="form-control" @change="load" />
          </div>
          <div class="col-12 col-md-2">
            <label class="form-label">Date To</label>
            <input v-model="filters.date_to" type="date" class="form-control" @change="load" />
          </div>
          <div class="col-12 col-md-2">
            <label class="form-label">Status</label>
            <select v-model="filters.status" class="form-select" @change="load">
              <option value="">All</option>
              <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </div>
          <div class="col-12 col-md-4">
            <label class="form-label">Search</label>
            <div class="input-icon-wrap">
              <i class="bi bi-search"></i>
              <input v-model="filters.search" type="text" class="form-control" placeholder="Patient, doctor, reason..." @input="debouncedSearch" />
            </div>
          </div>
          <div class="col-12 col-md-2 d-flex align-items-end">
            <button class="btn btn-outline-secondary w-100" @click="clearFilters"><i class="bi bi-x-circle"></i> Clear</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
        <div v-else-if="!appointments.length" class="empty-state">
          <i class="bi bi-calendar-x"></i><p>No appointments found</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table mb-0">
            <thead>
              <tr><th>Date & Time</th><th>Patient</th><th>Doctor</th><th>Treatment</th><th>Status</th><th>Actions</th></tr>
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
                    <span class="fw-600">{{ apt.patient_detail?.full_name }}</span>
                  </div>
                </td>
                <td>Dr. {{ apt.doctor_detail?.last_name }}</td>
                <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
                <td><span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span></td>
                <td>
                  <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-outline-primary" @click="openModal(apt)"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-sm btn-outline-warning" @click="quickStatus(apt.id, 'confirmed')" :disabled="apt.status === 'confirmed'"><i class="bi bi-check-circle"></i></button>
                    <button class="btn btn-sm btn-outline-danger" @click="cancelApt(apt.id)" :disabled="apt.status === 'cancelled'"><i class="bi bi-x-circle"></i></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modal.open" class="modal-overlay" @click.self="modal.open = false">
      <div class="modal-box modal-lg">
        <div class="modal-box-header">
          <h3><i class="bi bi-calendar-plus me-2"></i>{{ modal.editing ? 'Edit' : 'New' }} Appointment</h3>
          <button @click="modal.open = false" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-box-body">
          <div class="row g-3">
            <div class="col-12 col-md-6">
              <label class="form-label">Patient</label>
              <select v-model="form.patient" class="form-select">
                <option value="">Select patient...</option>
                <option v-for="p in patients" :key="p.id" :value="p.id">{{ p.full_name }}</option>
              </select>
            </div>
            <div class="col-12 col-md-6">
              <label class="form-label">Doctor</label>
              <select v-model="form.doctor" class="form-select">
                <option value="">Select doctor...</option>
                <option v-for="d in doctors" :key="d.id" :value="d.id">Dr. {{ d.full_name }}</option>
              </select>
            </div>
            <div class="col-12 col-md-4">
              <label class="form-label">Date</label>
              <input v-model="form.date" type="date" class="form-control" required />
            </div>
            <div class="col-12 col-md-4">
              <label class="form-label">Time</label>
              <input v-model="form.time" type="time" class="form-control" required />
            </div>
            <div class="col-12 col-md-4">
              <label class="form-label">Duration (min)</label>
              <input v-model="form.duration_minutes" type="number" min="15" max="180" step="15" class="form-control" />
            </div>
            <div class="col-12 col-md-6">
              <label class="form-label">Treatment Type</label>
              <select v-model="form.treatment_type" class="form-select">
                <option v-for="[k,v] in Object.entries(treatmentOptions)" :key="k" :value="k">{{ v }}</option>
              </select>
            </div>
            <div class="col-12 col-md-6">
              <label class="form-label">Status</label>
              <select v-model="form.status" class="form-select">
                <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label">Reason / Notes</label>
              <textarea v-model="form.reason" class="form-control" rows="3" placeholder="Reason for visit..."></textarea>
            </div>
          </div>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-outline-secondary" @click="modal.open = false">Cancel</button>
          <button class="btn btn-primary" @click="save" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            {{ modal.editing ? 'Update' : 'Book' }} Appointment
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
const patients = ref([])
const doctors = ref([])
const loading = ref(true)
const saving = ref(false)
const filters = ref({ date_from: '', date_to: '', status: '', search: '' })
const modal = ref({ open: false, editing: null })

const defaultForm = () => ({ patient: '', doctor: '', date: '', time: '', duration_minutes: 30, treatment_type: 'checkup', status: 'pending', reason: '' })
const form = ref(defaultForm())

const statuses = [
  { value: 'pending', label: 'Pending' },
  { value: 'confirmed', label: 'Confirmed' },
  { value: 'completed', label: 'Completed' },
  { value: 'cancelled', label: 'Cancelled' },
]

const treatmentOptions = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatments = treatmentOptions
const treatmentLabel = t => treatments[t] || t
const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
const formatDate = d => { try { return format(parseISO(d), 'MMM d, yyyy') } catch { return d } }

async function load() {
  loading.value = true
  const params = {}
  if (filters.value.date_from) params.date_from = filters.value.date_from
  if (filters.value.date_to) params.date_to = filters.value.date_to
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.search) params.search = filters.value.search
  try {
    const { data } = await api.get('/appointments/', { params })
    appointments.value = data.results || data
  } finally { loading.value = false }
}

let t = null
function debouncedSearch() { clearTimeout(t); t = setTimeout(load, 350) }
function clearFilters() { filters.value = { date_from: '', date_to: '', status: '', search: '' }; load() }

function openModal(apt = null) {
  if (apt) {
    form.value = { patient: apt.patient, doctor: apt.doctor, date: apt.date, time: apt.time?.slice(0,5), duration_minutes: apt.duration_minutes, treatment_type: apt.treatment_type, status: apt.status, reason: apt.reason }
    modal.value = { open: true, editing: apt.id }
  } else {
    form.value = defaultForm()
    modal.value = { open: true, editing: null }
  }
}

async function save() {
  if (!form.value.patient || !form.value.doctor || !form.value.date || !form.value.time) {
    toast.error('Please fill in all required fields.')
    return
  }
  saving.value = true
  try {
    if (modal.value.editing) {
      await api.patch(`/appointments/${modal.value.editing}/`, form.value)
      toast.success('Appointment updated!')
    } else {
      await api.post('/appointments/', form.value)
      toast.success('Appointment booked!')
    }
    modal.value.open = false
    load()
  } catch (e) {
    toast.error('Failed to save appointment.')
  } finally { saving.value = false }
}

async function quickStatus(id, status) {
  await api.patch(`/appointments/${id}/update_status/`, { status })
  toast.success(`Appointment ${status}.`)
  load()
}

async function cancelApt(id) {
  if (!confirm('Cancel this appointment?')) return
  await api.patch(`/appointments/${id}/update_status/`, { status: 'cancelled' })
  toast.info('Appointment cancelled.')
  load()
}

async function loadMeta() {
  const [pRes, dRes] = await Promise.all([api.get('/patients/'), api.get('/doctors/')])
  patients.value = pRes.data.results || pRes.data
  doctors.value = dRes.data.results || dRes.data
}

onMounted(() => { load(); loadMeta() })
</script>

<style scoped>
.datetime-cell { display: flex; flex-direction: column; }
.date { font-weight: 600; font-size: 0.88rem; }
.time { font-size: 0.78rem; color: var(--text-muted); }
.treatment-tag { background: #f1f5f9; color: #475569; padding: 3px 9px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; }
.fw-600 { font-weight: 600; font-size: 0.88rem; }
.input-icon-wrap { position: relative; }
.input-icon-wrap i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-icon-wrap .form-control { padding-left: 36px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 500; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal-box { background: white; border-radius: var(--radius-lg); width: 100%; max-width: 520px; box-shadow: var(--shadow-lg); }
.modal-lg { max-width: 680px; }
.modal-box-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border); }
.modal-box-header h3 { font-size: 1.05rem; font-weight: 700; margin: 0; }
.close-btn { background: none; border: none; font-size: 1rem; cursor: pointer; color: var(--text-muted); padding: 4px; }
.modal-box-body { padding: 24px; max-height: 65vh; overflow-y: auto; }
.modal-box-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 24px; border-top: 1px solid var(--border); }
</style>
