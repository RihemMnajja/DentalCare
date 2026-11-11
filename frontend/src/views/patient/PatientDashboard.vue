<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Hello, {{ auth.user?.first_name }} 👋</h1>
      <p class="page-subtitle">Here's your dental health overview</p>
    </div>

    <!-- Stats -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-xl-3">
        <div class="stat-card">
          <div class="stat-icon"><i class="bi bi-calendar-check"></i></div>
          <div class="stat-value">{{ data?.upcoming_count ?? '—' }}</div>
          <div class="stat-label">Upcoming Visits</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-green">
          <div class="stat-icon green"><i class="bi bi-check2-circle"></i></div>
          <div class="stat-value">{{ data?.total_completed ?? '—' }}</div>
          <div class="stat-label">Completed Visits</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-orange">
          <div class="stat-icon orange"><i class="bi bi-capsule"></i></div>
          <div class="stat-value">{{ activePrescriptions }}</div>
          <div class="stat-label">Active Prescriptions</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-teal">
          <div class="stat-icon teal"><i class="bi bi-journal-medical"></i></div>
          <div class="stat-value">{{ data?.medical_notes?.length ?? '—' }}</div>
          <div class="stat-label">Doctor Notes</div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <!-- Upcoming Appointments -->
      <div class="col-12 col-xl-7">
        <div class="card">
          <div class="card-header">
            <span><i class="bi bi-calendar3 me-2 text-primary"></i>Upcoming Appointments</span>
            <router-link to="/patient/appointments" class="btn btn-sm btn-outline-primary">See All</router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
            <div v-else-if="!data?.upcoming_appointments?.length" class="empty-state">
              <i class="bi bi-calendar-x"></i>
              <p>No upcoming appointments</p>
            </div>
            <div v-else class="apt-timeline">
              <div v-for="apt in data.upcoming_appointments" :key="apt.id" class="apt-card">
                <div class="apt-date-block">
                  <span class="apt-month">{{ formatMonth(apt.date) }}</span>
                  <span class="apt-day">{{ formatDay(apt.date) }}</span>
                </div>
                <div class="apt-body">
                  <div class="apt-title">{{ treatmentLabel(apt.treatment_type) }}</div>
                  <div class="apt-meta">
                    <span><i class="bi bi-clock"></i> {{ apt.time?.slice(0,5) }}</span>
                    <span><i class="bi bi-person-badge"></i> Dr. {{ apt.doctor_detail?.last_name }}</span>
                  </div>
                </div>
                <span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Prescriptions -->
      <div class="col-12 col-xl-5">
        <div class="card mb-4">
          <div class="card-header">
            <span><i class="bi bi-capsule me-2 text-primary"></i>Active Prescriptions</span>
            <router-link to="/patient/prescriptions" class="btn btn-sm btn-outline-primary">All</router-link>
          </div>
          <div class="card-body">
            <div v-if="!data?.prescriptions?.filter(p => p.is_active).length" class="empty-state">
              <i class="bi bi-file-earmark-x"></i>
              <p>No active prescriptions</p>
            </div>
            <div v-else class="rx-list">
              <div v-for="rx in data.prescriptions.filter(p => p.is_active)" :key="rx.id" class="rx-item">
                <div class="rx-icon"><i class="bi bi-capsule"></i></div>
                <div class="rx-info">
                  <strong>{{ rx.medication_name }}</strong>
                  <span>{{ rx.dosage }} · {{ rx.frequency }}</span>
                  <small>{{ rx.duration }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Notes -->
        <div class="card">
          <div class="card-header">
            <span><i class="bi bi-journal-medical me-2 text-primary"></i>Doctor Notes</span>
            <router-link to="/patient/notes" class="btn btn-sm btn-outline-primary">All</router-link>
          </div>
          <div class="card-body">
            <div v-if="!data?.medical_notes?.length" class="empty-state">
              <i class="bi bi-journal-x"></i>
              <p>No notes yet</p>
            </div>
            <div v-else class="notes-list">
              <div v-for="note in data.medical_notes.slice(0,3)" :key="note.id" class="note-item">
                <div class="note-type-dot" :class="`type-${note.note_type}`"></div>
                <div class="note-info">
                  <strong>{{ note.title }}</strong>
                  <span>{{ note.note_type }} · Dr. {{ note.doctor_detail?.last_name }}</span>
                  <small>{{ formatDate(note.date_created) }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { format, parseISO } from 'date-fns'

const auth = useAuthStore()
const data = ref(null)
const loading = ref(true)

const activePrescriptions = computed(() => data.value?.prescriptions?.filter(p => p.is_active).length ?? '—')

const treatments = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatmentLabel = t => treatments[t] || t

const formatMonth = d => { try { return format(parseISO(d), 'MMM').toUpperCase() } catch { return '' } }
const formatDay   = d => { try { return format(parseISO(d), 'd') } catch { return '' } }
const formatDate  = d => { try { return format(parseISO(d), 'MMM d, yyyy') } catch { return d } }

onMounted(async () => {
  try { const { data: res } = await api.get('/dashboard/'); data.value = res }
  finally { loading.value = false }
})
</script>

<style scoped>
.apt-timeline { display: flex; flex-direction: column; gap: 12px; }
.apt-card { display: flex; align-items: center; gap: 14px; padding: 14px; border-radius: 12px; background: #f8faff; border: 1px solid var(--border); transition: var(--transition); }
.apt-card:hover { border-color: var(--primary); background: var(--primary-light); }
.apt-date-block { display: flex; flex-direction: column; align-items: center; min-width: 46px; background: var(--primary); color: white; border-radius: 10px; padding: 6px; }
.apt-month { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; opacity: 0.85; }
.apt-day { font-size: 1.4rem; font-weight: 800; line-height: 1; }
.apt-body { flex: 1; }
.apt-title { font-weight: 700; font-size: 0.9rem; margin-bottom: 4px; }
.apt-meta { display: flex; gap: 12px; font-size: 0.78rem; color: var(--text-secondary); }
.apt-meta span { display: flex; align-items: center; gap: 4px; }

.rx-list { display: flex; flex-direction: column; gap: 10px; }
.rx-item { display: flex; align-items: center; gap: 10px; padding: 10px; background: #f8faff; border: 1px solid var(--border); border-radius: 10px; }
.rx-icon { width: 36px; height: 36px; background: rgba(26,111,196,0.1); color: var(--primary); border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.rx-info { display: flex; flex-direction: column; }
.rx-info strong { font-size: 0.88rem; font-weight: 700; }
.rx-info span { font-size: 0.78rem; color: var(--text-secondary); }
.rx-info small { font-size: 0.72rem; color: var(--text-muted); }

.notes-list { display: flex; flex-direction: column; gap: 10px; }
.note-item { display: flex; align-items: flex-start; gap: 10px; padding: 10px; background: #f8faff; border: 1px solid var(--border); border-radius: 10px; }
.note-type-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; margin-top: 5px; }
.type-diagnosis { background: var(--primary); }
.type-advice { background: var(--success); }
.type-observation { background: var(--accent-warm); }
.type-follow_up { background: var(--secondary); }
.note-info { display: flex; flex-direction: column; }
.note-info strong { font-size: 0.88rem; font-weight: 700; }
.note-info span { font-size: 0.78rem; color: var(--text-secondary); text-transform: capitalize; }
.note-info small { font-size: 0.72rem; color: var(--text-muted); }
</style>
