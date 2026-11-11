<template>
  <div class="app-layout">
    <AppSidebar :nav-groups="navGroups" :is-collapsed="collapsed" :mobile-open="mobileOpen"
      @toggle="collapsed = !collapsed" @close="mobileOpen = false" />
    <div class="mobile-overlay" v-if="mobileOpen" @click="mobileOpen = false"></div>
    <div class="main-content">
      <AppHeader @toggle-mobile="mobileOpen = !mobileOpen" />
      <div class="page-content">
        <transition name="slide-up" mode="out-in">
          <router-view :key="$route.path" />
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppSidebar from '@/components/AppSidebar.vue'
import AppHeader from '@/components/AppHeader.vue'

const collapsed = ref(false)
const mobileOpen = ref(false)

const navGroups = [
  {
    label: 'Overview',
    items: [
      { to: '/doctor/dashboard', icon: 'bi bi-grid-1x2', label: 'Dashboard' },
    ]
  },
  {
    label: 'Clinical',
    items: [
      { to: '/doctor/appointments', icon: 'bi bi-calendar-check', label: 'Appointments' },
      { to: '/doctor/patients', icon: 'bi bi-people', label: 'My Patients' },
      { to: '/doctor/prescriptions', icon: 'bi bi-file-medical', label: 'Prescriptions' },
    ]
  }
]
</script>

<style scoped>
.mobile-overlay {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 99;
}
@media (max-width: 768px) {
  .mobile-overlay { display: block; }
}
</style>
