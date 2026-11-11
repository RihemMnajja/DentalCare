<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed, 'mobile-open': mobileOpen }">
    <!-- Brand -->
    <div class="sidebar-brand">
      <div class="brand-icon"><i class="bi bi-hospital"></i></div>
      <span class="brand-name">DentalCare</span>
      <button class="collapse-btn" @click="$emit('toggle')">
        <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
      </button>
    </div>

    <!-- Role badge -->
    <div class="role-badge">
      <div class="role-avatar">
        <i :class="roleIcon"></i>
      </div>
      <div class="role-info">
        <span class="role-name">{{ auth.fullName }}</span>
        <span class="role-label">{{ auth.userRole }}</span>
      </div>
    </div>

    <!-- Nav Items -->
    <nav class="sidebar-nav">
      <div v-for="group in navGroups" :key="group.label" class="nav-group">
        <div class="nav-group-label">{{ group.label }}</div>
        <router-link
          v-for="item in group.items"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          :class="{ active: isActive(item.to) }"
        >
          <i :class="item.icon"></i>
          <span>{{ item.label }}</span>
          <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </div>
    </nav>

    <!-- Logout -->
    <div class="sidebar-footer">
      <button class="nav-item logout-btn" @click="handleLogout">
        <i class="bi bi-box-arrow-left"></i>
        <span>Sign Out</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const props = defineProps({
  navGroups: Array,
  isCollapsed: Boolean,
  mobileOpen: Boolean,
})
const emit = defineEmits(['toggle', 'close'])

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const roleIcon = computed(() => {
  const icons = { doctor: 'bi bi-person-badge', secretary: 'bi bi-person-workspace', patient: 'bi bi-person-heart' }
  return icons[auth.userRole] || 'bi bi-person'
})

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

async function handleLogout() {
  await auth.logout()
  toast.info('You have been signed out.')
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  position: fixed;
  left: 0; top: 0;
  background: var(--bg-sidebar);
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: var(--transition-slow);
  overflow: hidden;
}

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  min-height: var(--header-height);
}
.brand-icon {
  width: 36px; height: 36px;
  background: var(--primary);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 1rem;
  flex-shrink: 0;
}
.brand-name { color: white; font-weight: 800; font-size: 1.1rem; flex: 1; white-space: nowrap; }
.collapse-btn {
  background: rgba(255,255,255,0.06);
  border: none; color: rgba(255,255,255,0.5);
  width: 26px; height: 26px;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; font-size: 0.75rem;
  flex-shrink: 0;
  transition: var(--transition);
}
.collapse-btn:hover { background: rgba(255,255,255,0.12); color: white; }

/* Role Badge */
.role-badge {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.role-avatar {
  width: 38px; height: 38px;
  background: var(--primary);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 1rem;
  flex-shrink: 0;
}
.role-info { display: flex; flex-direction: column; min-width: 0; }
.role-name { color: white; font-weight: 600; font-size: 0.88rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.role-label { color: rgba(255,255,255,0.45); font-size: 0.72rem; text-transform: capitalize; }

/* Nav */
.sidebar-nav { flex: 1; padding: 12px 10px; overflow-y: auto; }
.nav-group { margin-bottom: 16px; }
.nav-group-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.3);
  padding: 4px 10px 6px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
  transition: var(--transition);
  margin-bottom: 2px;
  position: relative;
}
.nav-item i { font-size: 1.05rem; flex-shrink: 0; }
.nav-item span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nav-item:hover { background: var(--bg-sidebar-hover); color: white; }
.nav-item.active {
  background: var(--bg-sidebar-active);
  color: white;
}
.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0; top: 6px; bottom: 6px;
  width: 3px;
  background: var(--primary);
  border-radius: 0 3px 3px 0;
}
.nav-badge {
  margin-left: auto;
  background: var(--primary);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
  flex-shrink: 0;
}

/* Footer */
.sidebar-footer {
  padding: 12px 10px;
  border-top: 1px solid rgba(255,255,255,0.06);
}
.logout-btn {
  width: 100%; background: none; border: none; cursor: pointer;
  color: rgba(255,255,255,0.5);
}
.logout-btn:hover { background: rgba(239,68,68,0.12); color: #f87171; }

/* Mobile */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  .collapse-btn { display: none; }
}
</style>
