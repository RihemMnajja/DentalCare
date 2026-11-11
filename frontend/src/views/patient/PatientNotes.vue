<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Doctor Notes</h1>
      <p class="page-subtitle">Medical notes, advice and observations from your doctor</p>
    </div>

    <!-- Type Filter -->
    <div class="filter-row mb-4">
      <button class="filter-btn" :class="{ active: filter === 'all' }" @click="filter = 'all'">All Notes</button>
      <button v-for="t in noteTypes" :key="t.value" class="filter-btn" :class="{ active: filter === t.value }" @click="filter = t.value">
        <i :class="t.icon"></i> {{ t.label }}
      </button>
    </div>

    <div v-if="loading" class="empty-state"><div class="spinner-ring mx-auto"></div></div>
    <div v-else-if="!filtered.length" class="card">
      <div class="empty-state"><i class="bi bi-journal-x"></i><p>No notes found</p></div>
    </div>
    <div v-else class="notes-container">
      <div class="timeline">
        <div v-for="note in filtered" :key="note.id" class="timeline-item">
          <div class="timeline-dot" :class="`type-${note.note_type}`">
            <i :class="noteIcon(note.note_type)"></i>
          </div>
          <div class="timeline-content note-card">
            <div class="note-card-header">
              <div>
                <h4>{{ note.title }}</h4>
                <div class="note-meta">
                  <span class="note-type-badge" :class="`type-${note.note_type}`">{{ note.note_type }}</span>
                  <span><i class="bi bi-person-badge"></i> Dr. {{ note.doctor_detail?.last_name }}</span>
                  <span><i class="bi bi-clock"></i> {{ formatDate(note.date_created) }}</span>
                </div>
              </div>
            </div>
            <p class="note-content">{{ note.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'
import { format, parseISO } from 'date-fns'

const notes = ref([])
const loading = ref(true)
const filter = ref('all')

const noteTypes = [
  { value: 'diagnosis', label: 'Diagnosis', icon: 'bi bi-clipboard2-pulse' },
  { value: 'advice', label: 'Advice', icon: 'bi bi-chat-dots' },
  { value: 'observation', label: 'Observation', icon: 'bi bi-eye' },
  { value: 'follow_up', label: 'Follow-up', icon: 'bi bi-arrow-repeat' },
]

const filtered = computed(() => {
  if (filter.value === 'all') return notes.value
  return notes.value.filter(n => n.note_type === filter.value)
})

const noteIcon = t => ({ diagnosis:'bi bi-clipboard2-pulse', advice:'bi bi-chat-dots', observation:'bi bi-eye', follow_up:'bi bi-arrow-repeat' }[t] || 'bi bi-journal')
const formatDate = d => { try { return format(parseISO(d), 'MMM d, yyyy · h:mm a') } catch { return d } }

onMounted(async () => {
  try {
    const { data } = await api.get('/notes/')
    notes.value = data.results || data
  } finally { loading.value = false }
})
</script>

<style scoped>
.filter-row { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-btn { display: flex; align-items: center; gap: 6px; padding: 7px 16px; border: 1.5px solid var(--border); border-radius: 20px; font-size: 0.85rem; font-weight: 600; font-family: var(--font-sans); background: white; color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.filter-btn.active { background: var(--primary); color: white; border-color: var(--primary); }

.notes-container { padding-left: 8px; }

/* Override timeline-dot colors */
.timeline-dot.type-diagnosis { background: rgba(26,111,196,0.15); color: var(--primary); }
.timeline-dot.type-advice { background: rgba(16,185,129,0.15); color: var(--success); }
.timeline-dot.type-observation { background: rgba(245,158,11,0.15); color: var(--accent-warm); }
.timeline-dot.type-follow_up { background: rgba(14,165,233,0.15); color: var(--secondary); }

.note-card { background: white; }
.note-card-header { margin-bottom: 10px; }
.note-card-header h4 { font-size: 1rem; font-weight: 700; margin: 0 0 6px; }
.note-meta { display: flex; flex-wrap: wrap; gap: 10px; font-size: 0.78rem; color: var(--text-secondary); align-items: center; }
.note-meta span { display: flex; align-items: center; gap: 4px; }

.note-type-badge { padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; text-transform: capitalize; }
.type-diagnosis { background: rgba(26,111,196,0.1); color: var(--primary); }
.type-advice { background: rgba(16,185,129,0.1); color: var(--success); }
.type-observation { background: rgba(245,158,11,0.1); color: #b45309; }
.type-follow_up { background: rgba(14,165,233,0.1); color: var(--secondary); }

.note-content { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin: 0; }
</style>
