<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Secretary Dashboard</h1>
      <p class="page-subtitle">Manage appointments and patients for today</p>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6 col-xl-3">
        <div class="stat-card">
          <div class="stat-icon"><i class="bi bi-calendar-day"></i></div>
          <div class="stat-value">{{ stats?.appointments_today_count ?? '—' }}</div>
          <div class="stat-label">Today's Appointments</div>
        </div>
      </div>
      <div class="col-6 col-xl-3">
        <div class="stat-card accent-orange">
          <div class="stat-icon orange"><i class="bi bi-hourglass-split"></i></div>
          <div class="stat-value">{{ stats?.pending_count ?? '—' }}</div>
          <div class="stat-label">Pending Confirmation</div>
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
    </div>

    <div class="row g-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <span><i class="bi bi-calendar-check me-2 text-primary"></i>Today's Schedule</span>
            <router-link to="/secretary/appointments" class="btn btn-primary btn-sm">
              <i class="bi bi-plus-lg me-1"></i> New Appointment
            </router-link>
          </div>
          <div class="card-body p-0">
            <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
            <div v-else-if="!stats?.appointments_today?.length" class="empty-state">
              <i class="bi bi-calendar-x"></i><p>No appointments today</p>
            </div>
            <div v-else class="table-responsive">
              <table class="table mb-0">
                <thead>
                  <tr><th>Time</th><th>Patient</th><th>Doctor</th><th>Treatment</th><th>Status</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  <tr v-for="apt in stats.appointments_today" :key="apt.id">
                    <td><span class="time-badge">{{ apt.time?.slice(0,5) }}</span></td>
                    <td>
                      <div class="d-flex align-items-center gap-2">
                        <div class="avatar">{{ initials(apt.patient_detail) }}</div>
                        <div>
                          <div class="fw-600">{{ apt.patient_detail?.full_name }}</div>
                          <small class="text-muted">{{ apt.patient_detail?.phone }}</small>
                        </div>
                      </div>
                    </td>
                    <td>Dr. {{ apt.doctor_detail?.last_name }}</td>
                    <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
                    <td><span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span></td>
                    <td>
                      <div class="d-flex gap-1">
                        <router-link to="/secretary/appointments" class="btn btn-sm btn-outline-primary"><i class="bi bi-pencil"></i></router-link>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const stats = ref(null)
const loading = ref(true)

const treatments = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatmentLabel = t => treatments[t] || t
const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'

onMounted(async () => {
  try { const { data } = await api.get('/dashboard/'); stats.value = data }
  finally { loading.value = false }
})
</script>

<style scoped>
.time-badge { background: var(--primary-light); color: var(--primary); padding: 4px 10px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; }
.treatment-tag { background: #f1f5f9; color: #475569; padding: 3px 9px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; }
.fw-600 { font-weight: 600; font-size: 0.88rem; }
</style>
