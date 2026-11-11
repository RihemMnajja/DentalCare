<template>
  <div>
    <div class="page-header">
      <button class="btn btn-outline-secondary btn-sm mb-3" @click="$router.back()">
        <i class="bi bi-arrow-left me-1"></i> Back
      </button>
      <div v-if="patient" class="patient-banner">
        <div class="avatar avatar-lg">{{ initials(patient) }}</div>
        <div>
          <h1 class="page-title">{{ patient.full_name }}</h1>
          <p class="page-subtitle">{{ patient.email }} · {{ patient.phone || 'No phone' }}</p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="empty-state mt-5"><div class="spinner-ring mx-auto"></div></div>

    <div v-else class="row g-4">
      <!-- Patient Profile -->
      <div class="col-12 col-lg-4">
        <div class="card mb-4">
          <div class="card-header"><span><i class="bi bi-person-lines-fill me-2 text-primary"></i>Profile</span></div>
          <div class="card-body">
            <div v-if="patient?.patient_profile" class="profile-fields">
              <div class="pf-row"><span>Date of Birth</span><strong>{{ patient.patient_profile.date_of_birth || '—' }}</strong></div>
              <div class="pf-row"><span>Gender</span><strong>{{ genderLabel(patient.patient_profile.gender) }}</strong></div>
              <div class="pf-row"><span>Blood Type</span><strong>{{ patient.patient_profile.blood_type || '—' }}</strong></div>
              <div class="pf-row"><span>Emergency Contact</span><strong>{{ patient.patient_profile.emergency_contact || '—' }}</strong></div>
              <div class="pf-row"><span>Insurance #</span><strong>{{ patient.patient_profile.insurance_number || '—' }}</strong></div>
            </div>
            <div v-if="patient?.patient_profile?.allergies" class="mt-3">
              <label class="form-label">Allergies</label>
              <div class="info-box warning">{{ patient.patient_profile.allergies }}</div>
            </div>
            <div v-if="patient?.patient_profile?.medical_history" class="mt-3">
              <label class="form-label">Medical History</label>
              <div class="info-box">{{ patient.patient_profile.medical_history }}</div>
            </div>
          </div>
        </div>

        <!-- Quick actions -->
        <div class="card">
          <div class="card-header"><span><i class="bi bi-lightning me-2 text-primary"></i>Quick Actions</span></div>
          <div class="card-body d-flex flex-column gap-2">
            <button class="btn btn-outline-primary" @click="addNoteModal = true">
              <i class="bi bi-pencil-square me-1"></i> Add Medical Note
            </button>
            <button class="btn btn-outline-success" @click="addRxModal = true">
              <i class="bi bi-file-medical me-1"></i> Issue Prescription
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs: Appointments, Notes, Prescriptions -->
      <div class="col-12 col-lg-8">
        <div class="tabs-nav">
          <button v-for="tab in tabs" :key="tab.key" class="tab-btn" :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
            <i :class="tab.icon"></i> {{ tab.label }}
            <span class="tab-count">{{ tab.count }}</span>
          </button>
        </div>

        <!-- Appointments Tab -->
        <div v-if="activeTab === 'appointments'" class="card">
          <div class="card-body p-0">
            <div v-if="!appointments.length" class="empty-state"><i class="bi bi-calendar-x"></i><p>No appointments</p></div>
            <table v-else class="table mb-0">
              <thead><tr><th>Date</th><th>Treatment</th><th>Status</th><th>Notes</th></tr></thead>
              <tbody>
                <tr v-for="apt in appointments" :key="apt.id">
                  <td>{{ formatDate(apt.date) }} {{ apt.time?.slice(0,5) }}</td>
                  <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
                  <td><span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span></td>
                  <td>
                    <span v-if="apt.reason" class="text-muted small">{{ apt.reason.slice(0,40) }}...</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Notes Tab -->
        <div v-if="activeTab === 'notes'">
          <div v-if="!notes.length" class="card"><div class="empty-state"><i class="bi bi-journal-x"></i><p>No notes yet</p></div></div>
          <div v-else class="timeline mt-2">
            <div v-for="note in notes" :key="note.id" class="timeline-item">
              <div class="timeline-dot" :class="`note-${note.note_type}`">
                <i :class="noteIcon(note.note_type)"></i>
              </div>
              <div class="timeline-content">
                <div class="d-flex justify-content-between mb-1">
                  <strong>{{ note.title }}</strong>
                  <small class="text-muted">{{ formatDate(note.date_created) }}</small>
                </div>
                <span :class="['badge-status me-2', `badge-${note.note_type === 'diagnosis' ? 'confirmed' : 'pending'}`]">{{ note.note_type }}</span>
                <p class="mt-2 mb-0 small text-secondary">{{ note.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Prescriptions Tab -->
        <div v-if="activeTab === 'prescriptions'">
          <div v-if="!prescriptions.length" class="card"><div class="empty-state"><i class="bi bi-file-earmark-x"></i><p>No prescriptions</p></div></div>
          <div v-else class="rx-cards">
            <div v-for="rx in prescriptions" :key="rx.id" class="rx-card" :class="{ inactive: !rx.is_active }">
              <div class="rx-card-top">
                <div>
                  <h5>{{ rx.medication_name }}</h5>
                  <span class="rx-badge" :class="rx.is_active ? 'active' : 'inactive'">{{ rx.is_active ? 'Active' : 'Inactive' }}</span>
                </div>
                <span class="rx-date">{{ formatDate(rx.date_issued) }}</span>
              </div>
              <div class="rx-details">
                <div class="rx-detail-item"><i class="bi bi-capsule"></i> {{ rx.dosage }}</div>
                <div class="rx-detail-item"><i class="bi bi-clock"></i> {{ rx.frequency }}</div>
                <div class="rx-detail-item"><i class="bi bi-calendar-range"></i> {{ rx.duration }}</div>
              </div>
              <p v-if="rx.instructions" class="rx-instructions">{{ rx.instructions }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Note Modal -->
    <div v-if="addNoteModal" class="modal-overlay" @click.self="addNoteModal = false">
      <div class="modal-box">
        <div class="modal-box-header">
          <h3><i class="bi bi-pencil-square me-2"></i>Add Medical Note</h3>
          <button @click="addNoteModal = false" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-box-body">
          <div class="mb-3">
            <label class="form-label">Type</label>
            <select v-model="noteForm.note_type" class="form-select">
              <option value="diagnosis">Diagnosis</option>
              <option value="advice">Advice</option>
              <option value="observation">Observation</option>
              <option value="follow_up">Follow-up</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Title</label>
            <input v-model="noteForm.title" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Content</label>
            <textarea v-model="noteForm.content" class="form-control" rows="4"></textarea>
          </div>
          <div class="form-check">
            <input v-model="noteForm.is_private" class="form-check-input" type="checkbox" />
            <label class="form-check-label">Private note</label>
          </div>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-outline-secondary" @click="addNoteModal = false">Cancel</button>
          <button class="btn btn-primary" @click="saveNote" :disabled="saving">Save Note</button>
        </div>
      </div>
    </div>

    <!-- Add Rx Modal -->
    <div v-if="addRxModal" class="modal-overlay" @click.self="addRxModal = false">
      <div class="modal-box">
        <div class="modal-box-header">
          <h3><i class="bi bi-file-medical me-2"></i>Issue Prescription</h3>
          <button @click="addRxModal = false" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-box-body">
          <div class="mb-3"><label class="form-label">Medication</label><input v-model="rxForm.medication_name" type="text" class="form-control" /></div>
          <div class="row g-3 mb-3">
            <div class="col-6"><label class="form-label">Dosage</label><input v-model="rxForm.dosage" type="text" class="form-control" /></div>
            <div class="col-6"><label class="form-label">Frequency</label><input v-model="rxForm.frequency" type="text" class="form-control" /></div>
          </div>
          <div class="mb-3"><label class="form-label">Duration</label><input v-model="rxForm.duration" type="text" class="form-control" /></div>
          <div class="mb-3"><label class="form-label">Instructions</label><textarea v-model="rxForm.instructions" class="form-control" rows="3"></textarea></div>
        </div>
        <div class="modal-box-footer">
          <button class="btn btn-outline-secondary" @click="addRxModal = false">Cancel</button>
          <button class="btn btn-primary" @click="savePrescription" :disabled="saving">Issue</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'
import { format, parseISO } from 'date-fns'

const route = useRoute()
const toast = useToast()
const patientId = route.params.id

const patient = ref(null)
const appointments = ref([])
const notes = ref([])
const prescriptions = ref([])
const loading = ref(true)
const saving = ref(false)
const activeTab = ref('appointments')

const addNoteModal = ref(false)
const addRxModal = ref(false)
const noteForm = ref({ note_type: 'observation', title: '', content: '', is_private: false })
const rxForm = ref({ medication_name: '', dosage: '', frequency: '', duration: '', instructions: '' })

const tabs = computed(() => [
  { key: 'appointments', label: 'Appointments', icon: 'bi bi-calendar3', count: appointments.value.length },
  { key: 'notes', label: 'Notes', icon: 'bi bi-journal-medical', count: notes.value.length },
  { key: 'prescriptions', label: 'Prescriptions', icon: 'bi bi-file-medical', count: prescriptions.value.length },
])

const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
const formatDate = d => { try { return format(typeof d === 'string' && d.includes('T') ? parseISO(d) : parseISO(d + 'T00:00:00'), 'MMM d, yyyy') } catch { return d } }
const genderLabel = g => ({ M: 'Male', F: 'Female', O: 'Other' }[g] || '—')
const treatments = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatmentLabel = t => treatments[t] || t
const noteIcon = t => ({ diagnosis:'bi bi-clipboard2-pulse', advice:'bi bi-chat-dots', observation:'bi bi-eye', follow_up:'bi bi-arrow-repeat' }[t] || 'bi bi-journal')

async function loadAll() {
  loading.value = true
  const [pRes, aRes, nRes, rxRes] = await Promise.allSettled([
    api.get(`/patients/${patientId}/`),
    api.get('/appointments/', { params: { patient: patientId } }),
    api.get('/notes/', { params: { patient: patientId } }),
    api.get('/prescriptions/', { params: { patient: patientId } }),
  ])
  if (pRes.status === 'fulfilled') patient.value = pRes.value.data
  if (aRes.status === 'fulfilled') appointments.value = aRes.value.data.results || aRes.value.data
  if (nRes.status === 'fulfilled') notes.value = nRes.value.data.results || nRes.value.data
  if (rxRes.status === 'fulfilled') prescriptions.value = rxRes.value.data.results || rxRes.value.data
  loading.value = false
}

async function saveNote() {
  saving.value = true
  try {
    const { data } = await api.post('/notes/', { ...noteForm.value, patient: patientId })
    notes.value.unshift(data)
    toast.success('Note saved!')
    addNoteModal.value = false
  } catch { toast.error('Failed to save note.') }
  finally { saving.value = false }
}

async function savePrescription() {
  saving.value = true
  try {
    const { data } = await api.post('/prescriptions/', { ...rxForm.value, patient: patientId })
    prescriptions.value.unshift(data)
    toast.success('Prescription issued!')
    addRxModal.value = false
  } catch { toast.error('Failed to issue prescription.') }
  finally { saving.value = false }
}

onMounted(loadAll)
</script>

<style scoped>
.patient-banner { display: flex; align-items: center; gap: 16px; }
.profile-fields { display: flex; flex-direction: column; gap: 10px; }
.pf-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.88rem; padding: 8px 0; border-bottom: 1px solid var(--border); }
.pf-row span { color: var(--text-secondary); }
.pf-row strong { font-weight: 600; }
.info-box { background: #f8faff; border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; font-size: 0.85rem; color: var(--text-secondary); }
.info-box.warning { background: #fffbeb; border-color: #fde68a; color: #92400e; }

.tabs-nav { display: flex; gap: 4px; margin-bottom: 20px; background: white; border: 1px solid var(--border); border-radius: 10px; padding: 4px; }
.tab-btn { flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 9px; border: none; border-radius: 7px; font-size: 0.82rem; font-weight: 600; font-family: var(--font-sans); color: #64748b; background: transparent; cursor: pointer; transition: all 0.2s; }
.tab-btn.active { background: var(--primary); color: white; }
.tab-count { background: rgba(0,0,0,0.1); padding: 1px 7px; border-radius: 20px; font-size: 0.7rem; }
.tab-btn.active .tab-count { background: rgba(255,255,255,0.2); }

.treatment-tag { background: #f1f5f9; color: #475569; padding: 3px 9px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; }

.rx-cards { display: flex; flex-direction: column; gap: 14px; }
.rx-card { background: white; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 18px; transition: var(--transition); }
.rx-card.inactive { opacity: 0.6; }
.rx-card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.rx-card-top h5 { font-size: 1rem; font-weight: 700; margin: 0 0 6px; }
.rx-badge { padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.rx-badge.active { background: rgba(16,185,129,0.12); color: #065f46; }
.rx-badge.inactive { background: #f1f5f9; color: #64748b; }
.rx-date { font-size: 0.78rem; color: var(--text-muted); }
.rx-details { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 8px; }
.rx-detail-item { display: flex; align-items: center; gap: 5px; font-size: 0.82rem; color: var(--text-secondary); }
.rx-instructions { font-size: 0.82rem; color: var(--text-muted); background: #f8faff; border-radius: 6px; padding: 8px; margin: 0; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 500; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal-box { background: white; border-radius: var(--radius-lg); width: 100%; max-width: 520px; box-shadow: var(--shadow-lg); }
.modal-box-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--border); }
.modal-box-header h3 { font-size: 1.05rem; font-weight: 700; margin: 0; }
.close-btn { background: none; border: none; font-size: 1rem; cursor: pointer; color: var(--text-muted); padding: 4px; }
.modal-box-body { padding: 24px; max-height: 60vh; overflow-y: auto; }
.modal-box-footer { display: flex; justify-content: flex-end; gap: 10px; padding: 16px 24px; border-top: 1px solid var(--border); }
</style>
