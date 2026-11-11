<template>
  <header class="app-header">
    <div class="header-left">
      <button class="menu-toggle" @click="$emit('toggle-mobile')">
        <i class="bi bi-list"></i>
      </button>
      <div class="breadcrumb-path">
        <span class="page-name">{{ pageTitle }}</span>
      </div>
    </div>
    <div class="header-right">
      <div class="header-date">
        <i class="bi bi-calendar3"></i>
        {{ currentDate }}
      </div>
      <div class="header-user" @click="toggleDropdown" ref="dropdownRef">
        <div class="user-avatar">{{ initials }}</div>
        <div class="user-info">
          <span class="user-name">{{ auth.fullName }}</span>
          <span class="user-role">{{ auth.userRole }}</span>
        </div>
        <i class="bi bi-chevron-down chevron"></i>

        <div v-if="dropdownOpen" class="user-dropdown">
          <div class="dropdown-header">
            <div class="dh-avatar">{{ initials }}</div>
            <div>
              <strong>{{ auth.fullName }}</strong>
              <span>{{ auth.user?.email }}</span>
            </div>
          </div>
          <div class="dropdown-divider"></div>
          <!-- BUG FIX #4: route dynamique selon le rôle -->
          <router-link :to="`/${auth.userRole}/profile`" class="dropdown-item" @click="dropdownOpen = false">
            <i class="bi bi-person"></i> Mon Profil
          </router-link>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item text-danger" @click="logout">
            <i class="bi bi-box-arrow-left"></i> Déconnexion
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'

const emit = defineEmits(['toggle-mobile'])
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const dropdownOpen = ref(false)
const dropdownRef = ref(null)

const currentDate = computed(() => format(new Date(), 'EEEE, MMMM d, yyyy'))

const pageTitle = computed(() => {
  const name = route.name || ''
  return name.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
})

const initials = computed(() => {
  if (!auth.user) return '?'
  return `${auth.user.first_name?.[0] || ''}${auth.user.last_name?.[0] || ''}`.toUpperCase()
})

function toggleDropdown() { dropdownOpen.value = !dropdownOpen.value }

function handleClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    dropdownOpen.value = false
  }
}

async function logout() {
  await auth.logout()
  toast.info('Vous avez été déconnecté.')
  router.push('/login')
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.app-header {
  height: var(--header-height);
  background: white;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky; top: 0;
  z-index: 50;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.header-left { display: flex; align-items: center; gap: 16px; }
.menu-toggle { display: none; background: none; border: none; cursor: pointer; color: var(--text-secondary); font-size: 1.4rem; padding: 4px; border-radius: 6px; }
.menu-toggle:hover { color: var(--primary); background: var(--primary-light); }
.page-name { font-weight: 700; font-size: 1rem; color: var(--text-primary); }
.header-right { display: flex; align-items: center; gap: 20px; }
.header-date { display: flex; align-items: center; gap: 7px; font-size: 0.82rem; color: var(--text-muted); font-weight: 500; }
.header-date i { color: var(--primary); }
.header-user { display: flex; align-items: center; gap: 10px; cursor: pointer; padding: 6px 12px 6px 6px; border-radius: 40px; border: 1px solid var(--border); background: white; transition: var(--transition); position: relative; }
.header-user:hover { border-color: var(--primary); box-shadow: var(--shadow-primary); }
.user-avatar { width: 34px; height: 34px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; }
.user-info { display: flex; flex-direction: column; }
.user-name { font-size: 0.85rem; font-weight: 700; color: var(--text-primary); }
.user-role { font-size: 0.72rem; color: var(--text-muted); text-transform: capitalize; }
.chevron { font-size: 0.72rem; color: var(--text-muted); }
.user-dropdown { position: absolute; top: calc(100% + 10px); right: 0; width: 240px; background: white; border: 1px solid var(--border); border-radius: var(--radius-md); box-shadow: var(--shadow-lg); z-index: 200; overflow: hidden; }
.dropdown-header { display: flex; align-items: center; gap: 12px; padding: 16px; }
.dh-avatar { width: 40px; height: 40px; background: var(--primary-light); color: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem; }
.dropdown-header div { display: flex; flex-direction: column; }
.dropdown-header strong { font-size: 0.88rem; }
.dropdown-header span { font-size: 0.75rem; color: var(--text-muted); }
.dropdown-divider { height: 1px; background: var(--border); }
.dropdown-item { display: flex; align-items: center; gap: 10px; padding: 11px 16px; font-size: 0.88rem; color: var(--text-primary); text-decoration: none; background: none; border: none; width: 100%; cursor: pointer; font-family: var(--font-sans); transition: background 0.15s; }
.dropdown-item:hover { background: #f8faff; }
.dropdown-item.text-danger { color: var(--danger); }
.dropdown-item.text-danger:hover { background: #fef2f2; }
@media (max-width: 768px) {
  .menu-toggle { display: flex; }
  .header-date { display: none; }
  .user-info { display: none; }
  .chevron { display: none; }
  .app-header { padding: 0 16px; }
}
</style>
