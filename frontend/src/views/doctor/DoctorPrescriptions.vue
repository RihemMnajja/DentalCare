<template>
  <div>
    <div class="page-header d-flex justify-content-between align-items-start">
      <div>
        <h1 class="page-title">Prescriptions</h1>
        <p class="page-subtitle">All prescriptions you have issued</p>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-5">
            <div class="input-icon-wrap">
              <i class="bi bi-search"></i>
              <input v-model="search" type="text" class="form-control" placeholder="Search medication or patient..." @input="debouncedSearch" />
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="filterActive" class="form-select" @change="load">
              <option value="">All</option>
              <option value="true">Active Only</option>
              <option value="false">Inactive Only</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
    <div v-else-if="!prescriptions.length" class="empty-state card">
      <i class="bi bi-file-earmark-x"></i><p>No prescriptions found</p>
    </div>
    <div v-else class="rx-grid">
      <div v-for="rx in prescriptions" :key="rx.id" class="rx-card" :class="{ inactive: !rx.is_active }">
        <div class="rx-card-top">
          <div class="rx-icon"><i class="bi bi-capsule"></i></div>
          <div>
            <h5>{{ rx.medication_name }}</h5>
            <span class="rx-badge" :class="rx.is_active ? 'active' : 'inactive'">{{ rx.is_active ? 'Active' : 'Inactive' }}</span>
          </div>
          <div class="ms-auto text-end">
            <div class="rx-date">{{ formatDate(rx.date_issued) }}</div>
          </div>
        </div>

        <div class="rx-patient">
          <div class="avatar me-2">{{ initials(rx.patient_detail) }}</div>
          <span>{{ rx.patient_detail?.full_name }}</span>
        </div>

        <div class="rx-details">
          <div><i class="bi bi-capsule"></i> {{ rx.dosage }}</div>
          <div><i class="bi bi-clock"></i> {{ rx.frequency }}</div>
          <div><i class="bi bi-calendar-range"></i> {{ rx.duration }}</div>
        </div>
        <p v-if="rx.instructions" class="rx-instructions">{{ rx.instructions }}</p>

        <div class="rx-actions">
          <button class="btn btn-sm" :class="rx.is_active ? 'btn-outline-warning' : 'btn-outline-success'" @click="toggleActive(rx)">
            <i :class="rx.is_active ? 'bi bi-pause-circle' : 'bi bi-play-circle'"></i>
            {{ rx.is_active ? 'Deactivate' : 'Activate' }}
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
const prescriptions = ref([])
const loading = ref(true)
const search = ref('')
const filterActive = ref('')

const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
const formatDate = d => { try { return format(parseISO(d), 'MMM d, yyyy') } catch { return d } }

async function load() {
  loading.value = true
  const params = {}
  if (search.value) params.search = search.value
  if (filterActive.value !== '') params.is_active = filterActive.value
  try {
    const { data } = await api.get('/prescriptions/', { params })
    prescriptions.value = data.results || data
  } finally { loading.value = false }
}

let t = null
function debouncedSearch() { clearTimeout(t); t = setTimeout(load, 350) }

async function toggleActive(rx) {
  try {
    const { data } = await api.patch(`/prescriptions/${rx.id}/`, { is_active: !rx.is_active })
    rx.is_active = data.is_active
    toast.success(rx.is_active ? 'Prescription activated.' : 'Prescription deactivated.')
  } catch { toast.error('Failed to update.') }
}

onMounted(load)
</script>

<style scoped>
.rx-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }
.rx-card { background: white; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; transition: var(--transition); }
.rx-card.inactive { opacity: 0.65; }
.rx-card:hover { box-shadow: var(--shadow-md); }
.rx-card-top { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; }
.rx-icon { width: 42px; height: 42px; background: var(--primary-light); color: var(--primary); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
.rx-card-top h5 { font-size: 0.95rem; font-weight: 700; margin: 0 0 4px; }
.rx-badge { padding: 2px 9px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.rx-badge.active { background: rgba(16,185,129,0.12); color: #065f46; }
.rx-badge.inactive { background: #f1f5f9; color: #64748b; }
.rx-date { font-size: 0.78rem; color: var(--text-muted); }
.rx-patient { display: flex; align-items: center; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px; color: var(--text-secondary); }
.rx-details { display: flex; gap: 14px; flex-wrap: wrap; font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 8px; }
.rx-details div { display: flex; align-items: center; gap: 5px; }
.rx-instructions { font-size: 0.8rem; color: var(--text-muted); background: #f8faff; border-radius: 6px; padding: 8px; margin: 0 0 12px; }
.rx-actions { border-top: 1px solid var(--border); padding-top: 12px; }
.input-icon-wrap { position: relative; }
.input-icon-wrap i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-icon-wrap .form-control { padding-left: 36px; }
</style>
