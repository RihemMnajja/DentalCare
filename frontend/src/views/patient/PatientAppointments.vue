<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">My Appointments</h1>
      <p class="page-subtitle">View all your upcoming and past appointments</p>
    </div>

    <!-- Tabs -->
    <div class="tabs-nav mb-4">
      <button v-for="tab in tabs" :key="tab.key" class="tab-btn" :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
        <i :class="tab.icon"></i> {{ tab.label }}
        <span class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>

    <!-- Upcoming -->
    <div v-else-if="activeTab === 'upcoming'">
      <div v-if="!upcoming.length" class="card">
        <div class="empty-state"><i class="bi bi-calendar-x"></i><p>No upcoming appointments</p></div>
      </div>
      <div v-else class="appointments-grid">
        <div v-for="apt in upcoming" :key="apt.id" class="apt-detail-card">
          <div class="adc-header">
            <div class="adc-date">
              <i class="bi bi-calendar3"></i>
              <span>{{ formatDate(apt.date) }}</span>
            </div>
            <span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span>
          </div>
          <div class="adc-body">
            <div class="adc-treatment">{{ treatmentLabel(apt.treatment_type) }}</div>
            <div class="adc-meta">
              <span><i class="bi bi-clock"></i> {{ apt.time?.slice(0,5) }}</span>
              <span><i class="bi bi-stopwatch"></i> {{ apt.duration_minutes }} min</span>
              <span><i class="bi bi-person-badge"></i> Dr. {{ apt.doctor_detail?.last_name }}</span>
            </div>
            <p v-if="apt.reason" class="adc-reason">{{ apt.reason }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Past -->
    <div v-else-if="activeTab === 'past'">
      <div v-if="!past.length" class="card">
        <div class="empty-state"><i class="bi bi-clock-history"></i><p>No past appointments</p></div>
      </div>
      <div v-else class="card">
        <div class="card-body p-0">
          <table class="table mb-0">
            <thead><tr><th>Date</th><th>Treatment</th><th>Doctor</th><th>Duration</th><th>Status</th></tr></thead>
            <tbody>
              <tr v-for="apt in past" :key="apt.id">
                <td>
                  <div class="datetime-cell">
                    <span class="date">{{ formatDate(apt.date) }}</span>
                    <span class="time">{{ apt.time?.slice(0,5) }}</span>
                  </div>
                </td>
                <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
                <td>Dr. {{ apt.doctor_detail?.last_name }}</td>
                <td>{{ apt.duration_minutes }} min</td>
                <td><span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'
import { format, parseISO } from 'date-fns'

const upcoming = ref([])
const past = ref([])
const loading = ref(true)
const activeTab = ref('upcoming')

const treatments = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatmentLabel = t => treatments[t] || t
const formatDate = d => { try { return format(parseISO(d), 'EEEE, MMM d, yyyy') } catch { return d } }

const tabs = computed(() => [
  { key: 'upcoming', label: 'Upcoming', icon: 'bi bi-calendar-check', count: upcoming.value.length },
  { key: 'past', label: 'Past', icon: 'bi bi-clock-history', count: past.value.length },
])

onMounted(async () => {
  try {
    const today = format(new Date(), 'yyyy-MM-dd')
    const [upRes, pastRes] = await Promise.all([
      api.get('/appointments/', { params: { upcoming: 1 } }),
      api.get('/appointments/', { params: { status: 'completed' } }),
    ])
    upcoming.value = upRes.data.results || upRes.data
    past.value = pastRes.data.results || pastRes.data
  } finally { loading.value = false }
})
</script>

<style scoped>
.tabs-nav { display: flex; gap: 4px; background: white; border: 1px solid var(--border); border-radius: 10px; padding: 4px; width: fit-content; }
.tab-btn { display: flex; align-items: center; gap: 7px; padding: 9px 18px; border: none; border-radius: 7px; font-size: 0.88rem; font-weight: 600; font-family: var(--font-sans); color: #64748b; background: transparent; cursor: pointer; transition: all 0.2s; }
.tab-btn.active { background: var(--primary); color: white; }
.tab-count { background: rgba(0,0,0,0.1); padding: 1px 7px; border-radius: 20px; font-size: 0.72rem; }
.tab-btn.active .tab-count { background: rgba(255,255,255,0.2); }

.appointments-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }
.apt-detail-card { background: white; border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden; transition: var(--transition); }
.apt-detail-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.adc-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; background: #f8faff; border-bottom: 1px solid var(--border); }
.adc-date { display: flex; align-items: center; gap: 8px; font-size: 0.88rem; font-weight: 600; color: var(--text-primary); }
.adc-date i { color: var(--primary); }
.adc-body { padding: 16px 18px; }
.adc-treatment { font-size: 1rem; font-weight: 800; margin-bottom: 10px; }
.adc-meta { display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 10px; }
.adc-meta span { display: flex; align-items: center; gap: 5px; }
.adc-reason { font-size: 0.82rem; color: var(--text-muted); background: #f8faff; border-radius: 6px; padding: 8px 10px; margin: 0; }

.datetime-cell { display: flex; flex-direction: column; }
.date { font-weight: 600; font-size: 0.88rem; }
.time { font-size: 0.78rem; color: var(--text-muted); }
.treatment-tag { background: #f1f5f9; color: #475569; padding: 3px 9px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; }
</style>
