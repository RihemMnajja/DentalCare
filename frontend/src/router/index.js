import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Public
const LandingPage   = () => import('@/views/LandingPage.vue')
const LoginPage     = () => import('@/views/auth/LoginPage.vue')
const RegisterPage  = () => import('@/views/auth/RegisterPage.vue')

// Doctor
const DoctorLayout        = () => import('@/views/doctor/DoctorLayout.vue')
const DoctorDashboard     = () => import('@/views/doctor/DoctorDashboard.vue')
const DoctorAppointments  = () => import('@/views/doctor/DoctorAppointments.vue')
const DoctorPatients      = () => import('@/views/doctor/DoctorPatients.vue')
const PatientRecords      = () => import('@/views/doctor/PatientRecords.vue')
const DoctorPrescriptions = () => import('@/views/doctor/DoctorPrescriptions.vue')
const DoctorProfile       = () => import('@/views/doctor/DoctorProfile.vue')    // BUG FIX #5

// Secretary
const SecretaryLayout      = () => import('@/views/secretary/SecretaryLayout.vue')
const SecretaryDashboard   = () => import('@/views/secretary/SecretaryDashboard.vue')
const SecretaryAppointments = () => import('@/views/secretary/SecretaryAppointments.vue')
const SecretaryPatients    = () => import('@/views/secretary/SecretaryPatients.vue')
const SecretaryCalendar    = () => import('@/views/secretary/SecretaryCalendar.vue')
const SecretaryProfile     = () => import('@/views/secretary/SecretaryProfile.vue') // BUG FIX #5

// Patient
const PatientLayout       = () => import('@/views/patient/PatientLayout.vue')
const PatientDashboard    = () => import('@/views/patient/PatientDashboard.vue')
const PatientAppointments = () => import('@/views/patient/PatientAppointments.vue')
const PatientProfile      = () => import('@/views/patient/PatientProfile.vue')
const PatientPrescriptions = () => import('@/views/patient/PatientPrescriptions.vue')
const PatientNotes        = () => import('@/views/patient/PatientNotes.vue')

const routes = [
  { path: '/',         name: 'landing',  component: LandingPage,  meta: { public: true } },
  { path: '/login',    name: 'login',    component: LoginPage,    meta: { public: true } },
  { path: '/register', name: 'register', component: RegisterPage, meta: { public: true } },

  // ── Doctor ──
  {
    path: '/doctor',
    component: DoctorLayout,
    meta: { requiresAuth: true, role: 'doctor' },
    children: [
      { path: '',              redirect: '/doctor/dashboard' },
      { path: 'dashboard',    name: 'doctor-dashboard',    component: DoctorDashboard },
      { path: 'appointments', name: 'doctor-appointments', component: DoctorAppointments },
      { path: 'patients',     name: 'doctor-patients',     component: DoctorPatients },
      { path: 'patients/:id', name: 'patient-records',     component: PatientRecords },
      { path: 'prescriptions',name: 'doctor-prescriptions',component: DoctorPrescriptions },
      { path: 'profile',      name: 'doctor-profile',      component: DoctorProfile },   // FIX
    ]
  },

  // ── Secretary ──
  {
    path: '/secretary',
    component: SecretaryLayout,
    meta: { requiresAuth: true, role: 'secretary' },
    children: [
      { path: '',              redirect: '/secretary/dashboard' },
      { path: 'dashboard',    name: 'secretary-dashboard',    component: SecretaryDashboard },
      { path: 'appointments', name: 'secretary-appointments', component: SecretaryAppointments },
      { path: 'patients',     name: 'secretary-patients',     component: SecretaryPatients },
      { path: 'calendar',     name: 'secretary-calendar',     component: SecretaryCalendar },
      { path: 'profile',      name: 'secretary-profile',      component: SecretaryProfile }, // FIX
    ]
  },

  // ── Patient ──
  {
    path: '/patient',
    component: PatientLayout,
    meta: { requiresAuth: true, role: 'patient' },
    children: [
      { path: '',              redirect: '/patient/dashboard' },
      { path: 'dashboard',    name: 'patient-dashboard',    component: PatientDashboard },
      { path: 'appointments', name: 'patient-appointments', component: PatientAppointments },
      { path: 'profile',      name: 'patient-profile',      component: PatientProfile },
      { path: 'prescriptions',name: 'patient-prescriptions',component: PatientPrescriptions },
      { path: 'notes',        name: 'patient-notes',        component: PatientNotes },
    ]
  },

  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.public) {
    if (auth.isAuthenticated && ['login','register','landing'].includes(to.name)) {
      return next(`/${auth.userRole}`)
    }
    return next()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  if (to.meta.role && auth.userRole !== to.meta.role && auth.userRole !== 'admin') {
    return next(`/${auth.userRole || ''}`)
  }

  next()
})

export default router
