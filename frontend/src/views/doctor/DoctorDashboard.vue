<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Good {{ greeting }}, Dr. {{ auth.user?.last_name }} 👋</h1>
      <p class="page-subtitle">Here's your clinical overview for today</p>
    </div>

    <!-- Stats Row -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-xl-3">
        <div class="stat-card">
          <div class="stat-icon"><i class="bi bi-calendar-day"></i></div>
          <div class="stat-value">{{ stats?.appointments_today_count ?? '—' }}</div>
          <div class="stat-label">Today's Appointments</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-green">
          <div class="stat-icon green"><i class="bi bi-calendar-range"></i></div>
          <div class="stat-value">{{ stats?.upcoming_count ?? '—' }}</div>
          <div class="stat-label">Upcoming</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-teal">
          <div class="stat-icon teal"><i class="bi bi-people"></i></div>
          <div class="stat-value">{{ stats?.total_patients ?? '—' }}</div>
          <div class="stat-label">Total Patients</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-orange">
          <div class="stat-icon orange"><i class="bi bi-file-medical"></i></div>
          <div class="stat-value">{{ stats?.recent_prescriptions?.length ?? '—' }}</div>
          <div class="stat-label">Recent Prescriptions</div>
        </div>
      </div>
    </div>

    <!-- Today's Appointments + Prescriptions -->
    <div class="row g-4">
      <div class="col-12 col-xl-7">
        <div class="card">
          <div class="card-header">
            <span><i class="bi bi-calendar-check me-2 text-primary"></i>Today's Appointments</span>
            <router-link to="/doctor/appointments" class="btn btn-sm btn-outline-primary">View All</router-link>
          </div>
          <div class="card-body p-0">
            <div v-if="loading" class="empty-state">
              <div class="spinner-ring mx-auto"></div>
            </div>
            <div v-else-if="!stats?.appointments_today?.length" class="empty-state">
              <i class="bi bi-calendar-x"></i>
              <p>No appointments scheduled for today</p>
            </div>
            <div v-else>
              <table class="table mb-0">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Patient</th>
                    <th>Treatment</th>
                    <th>Status</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="apt in stats.appointments_today" :key="apt.id">
                    <td>
                      <span class="time-badge">{{ formatTime(apt.time) }}</span>
                    </td>
                    <td>
                      <div class="d-flex align-items-center gap-2">
                        <div class="avatar">{{ initials(apt.patient_detail) }}</div>
                        <span class="fw-600">{{ apt.patient_detail?.full_name }}</span>
                      </div>
                    </td>
                    <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
                    <td><span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span></td>
                    <td>
                      <router-link :to="`/doctor/patients/${apt.patient}`" class="btn btn-sm btn-outline-primary">
                        <i class="bi bi-eye"></i>
                      </router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-xl-5">
        <div class="card h-100">
          <div class="card-header">
            <span><i class="bi bi-file-medical me-2 text-primary"></i>Recent Prescriptions</span>
            <router-link to="/doctor/prescriptions" class="btn btn-sm btn-outline-primary">View All</router-link>
          </div>
          <div class="card-body">
            <div v-if="!stats?.recent_prescriptions?.length" class="empty-state">
              <i class="bi bi-file-earmark-x"></i>
              <p>No recent prescriptions</p>
            </div>
            <div v-else class="prescription-list">
              <div v-for="rx in stats.recent_prescriptions" :key="rx.id" class="rx-item">
                <div class="rx-icon"><i class="bi bi-capsule"></i></div>
                <div class="rx-info">
                  <strong>{{ rx.medication_name }}</strong>
                  <span>{{ rx.patient_detail?.full_name }} · {{ rx.dosage }}</span>
                  <small>{{ formatDate(rx.date_issued) }}</small>
                </div>
                <span v-if="rx.is_active" class="rx-active">Active</span>
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
const stats = ref(null)
const loading = ref(true)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
})

const treatments = {
  checkup: 'Checkup', cleaning: 'Cleaning', filling: 'Filling',
  extraction: 'Extraction', root_canal: 'Root Canal', crown: 'Crown',
  whitening: 'Whitening', braces: 'Braces', implant: 'Implant',
  emergency: 'Emergency', other: 'Other'
}

function treatmentLabel(t) { return treatments[t] || t }
function initials(u) { return u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?' }
function formatTime(t) { return t ? t.slice(0, 5) : '' }
function formatDate(d) { try { return format(parseISO(d), 'MMM d, yyyy') } catch { return d } }

onMounted(async () => {
  try {
    const { data } = await api.get('/dashboard/')
    stats.value = data
  } finally { loading.value = false }
})
</script>

<style scoped>
.time-badge {
  background: var(--primary-light);
  color: var(--primary);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 700;
}
.treatment-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 3px 9px;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
}
.fw-600 { font-weight: 600; font-size: 0.9rem; }

.prescription-list { display: flex; flex-direction: column; gap: 12px; }
.rx-item { display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 10px; background: #f8faff; border: 1px solid var(--border); }
.rx-icon { width: 38px; height: 38px; background: rgba(26,111,196,0.1); color: var(--primary); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.rx-info { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.rx-info strong { font-size: 0.88rem; font-weight: 700; }
.rx-info span { font-size: 0.78rem; color: var(--text-secondary); }
.rx-info small { font-size: 0.72rem; color: var(--text-muted); }
.rx-active { background: rgba(16,185,129,0.12); color: #065f46; padding: 2px 8px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; flex-shrink: 0; }
</style>
