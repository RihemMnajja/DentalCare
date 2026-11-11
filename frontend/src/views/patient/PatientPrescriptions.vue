<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">My Prescriptions</h1>
      <p class="page-subtitle">Medications prescribed by your doctor</p>
    </div>

    <!-- Filter -->
    <div class="filter-row mb-4">
      <button class="filter-btn" :class="{ active: filter === 'all' }" @click="filter = 'all'">All</button>
      <button class="filter-btn" :class="{ active: filter === 'active' }" @click="filter = 'active'">
        <span class="dot dot-active"></span> Active
      </button>
      <button class="filter-btn" :class="{ active: filter === 'inactive' }" @click="filter = 'inactive'">
        <span class="dot dot-inactive"></span> Inactive
      </button>
    </div>

    <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
    <div v-else-if="!filtered.length" class="card">
      <div class="empty-state"><i class="bi bi-file-earmark-x"></i><p>No prescriptions found</p></div>
    </div>
    <div v-else class="rx-grid">
      <div v-for="rx in filtered" :key="rx.id" class="rx-card" :class="{ inactive: !rx.is_active }">
        <div class="rx-card-top">
          <div class="rx-icon-wrap">
            <i class="bi bi-capsule-pill"></i>
          </div>
          <div class="rx-card-title">
            <h4>{{ rx.medication_name }}</h4>
            <span :class="['rx-status', rx.is_active ? 'active' : 'inactive']">
              <span class="dot" :class="rx.is_active ? 'dot-active' : 'dot-inactive'"></span>
              {{ rx.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <div class="rx-date">{{ formatDate(rx.date_issued) }}</div>
        </div>

        <div class="rx-info-grid">
          <div class="rx-info-item">
            <span>Dosage</span>
            <strong>{{ rx.dosage }}</strong>
          </div>
          <div class="rx-info-item">
            <span>Frequency</span>
            <strong>{{ rx.frequency }}</strong>
          </div>
          <div class="rx-info-item">
            <span>Duration</span>
            <strong>{{ rx.duration }}</strong>
          </div>
          <div class="rx-info-item">
            <span>Doctor</span>
            <strong>Dr. {{ rx.doctor_detail?.last_name }}</strong>
          </div>
        </div>

        <div v-if="rx.instructions" class="rx-instructions">
          <i class="bi bi-info-circle me-1"></i>
          {{ rx.instructions }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'
import { format, parseISO } from 'date-fns'

const prescriptions = ref([])
const loading = ref(true)
const filter = ref('all')

const filtered = computed(() => {
  if (filter.value === 'active') return prescriptions.value.filter(p => p.is_active)
  if (filter.value === 'inactive') return prescriptions.value.filter(p => !p.is_active)
  return prescriptions.value
})

const formatDate = d => { try { return format(parseISO(d), 'MMM d, yyyy') } catch { return d } }

onMounted(async () => {
  try {
    const { data } = await api.get('/prescriptions/')
    prescriptions.value = data.results || data
  } finally { loading.value = false }
})
</script>

<style scoped>
.filter-row { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-btn { display: flex; align-items: center; gap: 6px; padding: 7px 16px; border: 1.5px solid var(--border); border-radius: 20px; font-size: 0.85rem; font-weight: 600; font-family: var(--font-sans); background: white; color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.filter-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.dot-active { background: var(--success); }
.dot-inactive { background: #94a3b8; }

.rx-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }
.rx-card { background: white; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; transition: var(--transition); }
.rx-card:hover { box-shadow: var(--shadow-md); }
.rx-card.inactive { opacity: 0.65; }
.rx-card-top { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px; }
.rx-icon-wrap { width: 44px; height: 44px; background: var(--primary-light); color: var(--primary); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }
.rx-card-title { flex: 1; }
.rx-card-title h4 { font-size: 1rem; font-weight: 700; margin: 0 0 5px; }
.rx-status { display: inline-flex; align-items: center; gap: 5px; font-size: 0.75rem; font-weight: 600; }
.rx-status.active { color: var(--success); }
.rx-status.inactive { color: #94a3b8; }
.rx-date { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; }

.rx-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
.rx-info-item { background: #f8faff; border-radius: 8px; padding: 10px 12px; }
.rx-info-item span { display: block; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); font-weight: 700; margin-bottom: 3px; }
.rx-info-item strong { font-size: 0.88rem; font-weight: 700; }
.rx-instructions { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 12px; font-size: 0.82rem; color: #92400e; }
</style>
