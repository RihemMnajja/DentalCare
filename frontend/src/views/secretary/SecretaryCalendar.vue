<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Appointment Calendar</h1>
      <p class="page-subtitle">Visual overview of all scheduled appointments</p>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="cal-nav">
          <button class="btn btn-sm btn-outline-primary" @click="prevMonth"><i class="bi bi-chevron-left"></i></button>
          <h4>{{ monthName }} {{ currentYear }}</h4>
          <button class="btn btn-sm btn-outline-primary" @click="nextMonth"><i class="bi bi-chevron-right"></i></button>
        </div>
        <button class="btn btn-sm btn-primary" @click="goToday">Today</button>
      </div>
      <div class="card-body p-0">
        <!-- Day Labels -->
        <div class="cal-grid-header">
          <div v-for="d in dayLabels" :key="d" class="cal-day-label">{{ d }}</div>
        </div>
        <!-- Calendar Grid -->
        <div class="cal-grid">
          <div
            v-for="cell in calCells"
            :key="cell.key"
            class="cal-cell"
            :class="{ 'other-month': !cell.current, 'today': cell.isToday, 'selected': cell.date === selectedDate }"
            @click="selectDay(cell)"
          >
            <span class="cal-num">{{ cell.day }}</span>
            <div class="cal-dots">
              <span
                v-for="apt in cell.appointments.slice(0,3)"
                :key="apt.id"
                :class="['cal-dot', `dot-${apt.status}`]"
              ></span>
              <span v-if="cell.appointments.length > 3" class="cal-more">+{{ cell.appointments.length - 3 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected day appointments -->
    <div v-if="selectedDate" class="card mt-4">
      <div class="card-header">
        <span><i class="bi bi-calendar-day me-2 text-primary"></i>{{ formatSelectedDate }}</span>
        <span class="count-badge">{{ selectedApts.length }} appointments</span>
      </div>
      <div class="card-body p-0">
        <div v-if="!selectedApts.length" class="empty-state"><i class="bi bi-calendar-x"></i><p>No appointments</p></div>
        <table v-else class="table mb-0">
          <thead><tr><th>Time</th><th>Patient</th><th>Doctor</th><th>Treatment</th><th>Status</th></tr></thead>
          <tbody>
            <tr v-for="apt in selectedApts" :key="apt.id">
              <td><span class="time-badge">{{ apt.time?.slice(0,5) }}</span></td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="avatar">{{ initials(apt.patient_detail) }}</div>
                  <span class="fw-600">{{ apt.patient_detail?.full_name }}</span>
                </div>
              </td>
              <td>Dr. {{ apt.doctor_detail?.last_name }}</td>
              <td><span class="treatment-tag">{{ treatmentLabel(apt.treatment_type) }}</span></td>
              <td><span :class="['badge-status', `badge-${apt.status}`]">{{ apt.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'
import { format, parseISO, startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, isSameMonth, isToday } from 'date-fns'

const appointments = ref([])
const currentDate = ref(new Date())
const selectedDate = ref(null)

const dayLabels = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
const treatments = { checkup:'Checkup', cleaning:'Cleaning', filling:'Filling', extraction:'Extraction', root_canal:'Root Canal', crown:'Crown', whitening:'Whitening', braces:'Braces', implant:'Implant', emergency:'Emergency', other:'Other' }
const treatmentLabel = t => treatments[t] || t
const initials = u => u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'

const currentYear = computed(() => currentDate.value.getFullYear())
const monthName = computed(() => format(currentDate.value, 'MMMM'))

const calCells = computed(() => {
  const start = startOfWeek(startOfMonth(currentDate.value))
  const end = endOfWeek(endOfMonth(currentDate.value))
  return eachDayOfInterval({ start, end }).map(day => {
    const dateStr = format(day, 'yyyy-MM-dd')
    return {
      key: dateStr,
      day: day.getDate(),
      date: dateStr,
      current: isSameMonth(day, currentDate.value),
      isToday: isToday(day),
      appointments: appointments.value.filter(a => a.date === dateStr),
    }
  })
})

const selectedApts = computed(() => {
  if (!selectedDate.value) return []
  return appointments.value.filter(a => a.date === selectedDate.value).sort((a,b) => a.time.localeCompare(b.time))
})

const formatSelectedDate = computed(() => {
  if (!selectedDate.value) return ''
  try { return format(parseISO(selectedDate.value), 'EEEE, MMMM d, yyyy') } catch { return selectedDate.value }
})

function prevMonth() { const d = new Date(currentDate.value); d.setMonth(d.getMonth() - 1); currentDate.value = d; load() }
function nextMonth() { const d = new Date(currentDate.value); d.setMonth(d.getMonth() + 1); currentDate.value = d; load() }
function goToday() { currentDate.value = new Date(); selectedDate.value = format(new Date(), 'yyyy-MM-dd'); load() }
function selectDay(cell) { selectedDate.value = cell.date }

async function load() {
  const from = format(startOfMonth(currentDate.value), 'yyyy-MM-dd')
  const to = format(endOfMonth(currentDate.value), 'yyyy-MM-dd')
  const { data } = await api.get('/appointments/', { params: { date_from: from, date_to: to, page_size: 200 } })
  appointments.value = data.results || data
}

onMounted(() => { selectedDate.value = format(new Date(), 'yyyy-MM-dd'); load() })
</script>

<style scoped>
.cal-nav { display: flex; align-items: center; gap: 16px; }
.cal-nav h4 { margin: 0; font-size: 1rem; font-weight: 700; min-width: 160px; text-align: center; }
.cal-grid-header { display: grid; grid-template-columns: repeat(7, 1fr); background: #f8faff; border-bottom: 1px solid var(--border); }
.cal-day-label { text-align: center; padding: 10px; font-size: 0.78rem; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); }
.cal-cell { min-height: 90px; padding: 8px; border-right: 1px solid var(--border); border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.15s; }
.cal-cell:nth-child(7n) { border-right: none; }
.cal-cell:hover { background: var(--primary-light); }
.cal-cell.other-month { background: #fafafa; }
.cal-cell.other-month .cal-num { color: #cbd5e1; }
.cal-cell.today .cal-num { background: var(--primary); color: white; border-radius: 50%; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; }
.cal-cell.selected { background: var(--primary-light); border: 2px solid var(--primary); }
.cal-num { font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
.cal-dots { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 4px; }
.cal-dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-pending { background: var(--accent-warm); }
.dot-confirmed { background: var(--success); }
.dot-cancelled { background: var(--danger); }
.dot-completed { background: var(--primary); }
.dot-no_show { background: var(--text-muted); }
.cal-more { font-size: 0.68rem; color: var(--primary); font-weight: 700; }
.count-badge { background: var(--primary-light); color: var(--primary); padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
.time-badge { background: var(--primary-light); color: var(--primary); padding: 4px 10px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; }
.treatment-tag { background: #f1f5f9; color: #475569; padding: 3px 9px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; }
.fw-600 { font-weight: 600; font-size: 0.88rem; }
</style>
