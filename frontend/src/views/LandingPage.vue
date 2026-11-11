<template>
  <div class="landing">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-bg">
        <div class="hero-blob blob-1"></div>
        <div class="hero-blob blob-2"></div>
        <div class="hero-grid"></div>
      </div>
      <nav class="landing-nav">
        <div class="nav-brand">
          <div class="brand-icon"><i class="bi bi-hospital"></i></div>
          <span class="brand-name">DentalCare</span>
        </div>
        <div class="nav-actions">
          <router-link to="/login" class="btn btn-outline-primary btn-sm">Sign In</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">Get Started</router-link>
        </div>
      </nav>

      <div class="hero-content">
        <div class="hero-badge">
          <i class="bi bi-stars"></i>
          Professional Dental Management
        </div>
        <h1 class="hero-title">
          Welcome to<br>
          <span class="title-accent">Dental Care</span><br>
          Appointment System
        </h1>
        <p class="hero-desc">
          A modern, secure platform connecting doctors, secretaries, and patients.
          Manage appointments, prescriptions, and medical records in one place.
        </p>
        <div class="hero-cta">
          <router-link to="/register" class="btn btn-primary btn-lg">
            <i class="bi bi-arrow-right-circle"></i> Get Started Free
          </router-link>
          <router-link to="/login" class="btn btn-ghost btn-lg">
            <i class="bi bi-box-arrow-in-right"></i> Sign In
          </router-link>
        </div>
      </div>

      <div class="hero-visual">
        <div class="visual-card vc-1">
          <i class="bi bi-calendar-check"></i>
          <div><strong>Today's Appointments</strong><span>8 scheduled</span></div>
        </div>
        <div class="visual-card vc-2">
          <i class="bi bi-person-check"></i>
          <div><strong>Patients Served</strong><span>1,240+</span></div>
        </div>
        <div class="visual-card vc-3">
          <i class="bi bi-shield-check"></i>
          <div><strong>Secure & Private</strong><span>HIPAA compliant</span></div>
        </div>
      </div>
    </div>

    <!-- Role Section -->
    <div class="roles-section">
      <div class="section-header">
        <h2>Choose Your Role</h2>
        <p>Each role has a dedicated dashboard tailored to your workflow</p>
      </div>
      <div class="roles-grid">
        <div v-for="role in roles" :key="role.key" class="role-card" :class="`role-${role.key}`">
          <div class="role-icon">
            <i :class="role.icon"></i>
          </div>
          <h3>{{ role.title }}</h3>
          <p>{{ role.description }}</p>
          <ul>
            <li v-for="feat in role.features" :key="feat">
              <i class="bi bi-check2"></i> {{ feat }}
            </li>
          </ul>
          <router-link :to="`/register?role=${role.key}`" class="role-btn">
            Register as {{ role.title }}
            <i class="bi bi-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Features -->
    <div class="features-section">
      <div class="section-header">
        <h2>Everything You Need</h2>
        <p>Powerful tools for efficient dental practice management</p>
      </div>
      <div class="features-grid">
        <div v-for="feat in features" :key="feat.title" class="feature-item">
          <div class="feature-icon">
            <i :class="feat.icon"></i>
          </div>
          <h4>{{ feat.title }}</h4>
          <p>{{ feat.desc }}</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="footer-brand">
        <div class="brand-icon"><i class="bi bi-hospital"></i></div>
        <span>DentalCare</span>
      </div>
      <p>© 2025 DentalCare Management System. Built with Vue.js & Django.</p>
    </footer>
  </div>
</template>

<script setup>
const roles = [
  {
    key: 'doctor',
    title: 'Doctor',
    icon: 'bi bi-person-badge',
    description: 'Full clinical management with patient records and prescriptions.',
    features: ['View daily appointments', 'Write prescriptions', 'Add medical notes', 'Patient history']
  },
  {
    key: 'secretary',
    title: 'Secretary',
    icon: 'bi bi-person-workspace',
    description: 'Comprehensive scheduling and patient administration tools.',
    features: ['Schedule appointments', 'Calendar view', 'Manage patients', 'Edit & cancel bookings']
  },
  {
    key: 'patient',
    title: 'Patient',
    icon: 'bi bi-person-heart',
    description: 'Transparent access to your appointments and medical records.',
    features: ['View upcoming visits', 'See prescriptions', 'Read doctor advice', 'Track history']
  }
]

const features = [
  { icon: 'bi bi-lock-fill', title: 'Secure Authentication', desc: 'JWT-based login with role-based access control.' },
  { icon: 'bi bi-calendar3', title: 'Smart Scheduling', desc: 'Intuitive calendar with conflict detection.' },
  { icon: 'bi bi-file-medical', title: 'Digital Prescriptions', desc: 'Issue and manage prescriptions digitally.' },
  { icon: 'bi bi-clipboard2-pulse', title: 'Medical Records', desc: 'Complete patient history at your fingertips.' },
  { icon: 'bi bi-bell', title: 'Status Tracking', desc: 'Real-time appointment status updates.' },
  { icon: 'bi bi-phone', title: 'Fully Responsive', desc: 'Works perfectly on desktop and mobile.' },
]
</script>

<style scoped>
.landing { min-height: 100vh; background: #fff; overflow-x: hidden; }

/* ── Hero ── */
.hero {
  min-height: 100vh;
  background: linear-gradient(135deg, #0d1b2e 0%, #1a3a5c 60%, #1a6fc4 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding-bottom: 80px;
}

.hero-bg { position: absolute; inset: 0; pointer-events: none; }
.hero-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.25;
}
.blob-1 {
  width: 600px; height: 600px;
  background: #1a6fc4;
  top: -200px; right: -200px;
  animation: float 8s ease-in-out infinite;
}
.blob-2 {
  width: 400px; height: 400px;
  background: #06d6a0;
  bottom: -100px; left: -100px;
  animation: float 10s ease-in-out infinite reverse;
}
.hero-grid {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
}
@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-20px, 20px); }
}

/* Nav */
.landing-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 24px 60px;
  position: relative; z-index: 10;
}
.nav-brand { display: flex; align-items: center; gap: 12px; }
.brand-icon {
  width: 40px; height: 40px;
  background: rgba(255,255,255,0.15);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 1.2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}
.brand-name { color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: -0.02em; }
.nav-actions { display: flex; gap: 12px; }
.nav-actions .btn-outline-primary {
  border-color: rgba(255,255,255,0.4); color: white; background: rgba(255,255,255,0.08);
  backdrop-filter: blur(10px);
}
.nav-actions .btn-outline-primary:hover { background: rgba(255,255,255,0.2); }
.nav-actions .btn-primary { background: white; color: var(--primary); box-shadow: none; }
.nav-actions .btn-primary:hover { background: rgba(255,255,255,0.9); color: var(--primary); transform: translateY(-1px); }

/* Hero Content */
.hero-content {
  flex: 1;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  padding: 60px 40px 40px;
  position: relative; z-index: 10;
}

.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.9);
  padding: 8px 18px;
  border-radius: 40px;
  font-size: 0.85rem; font-weight: 600;
  margin-bottom: 32px;
  backdrop-filter: blur(10px);
}

.hero-title {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 800;
  color: white;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -0.03em;
}
.title-accent {
  background: linear-gradient(135deg, #5bc4ff, #06d6a0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 1.1rem; color: rgba(255,255,255,0.7);
  max-width: 520px; line-height: 1.7;
  margin-bottom: 40px;
}

.hero-cta { display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }
.btn-ghost {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  backdrop-filter: blur(10px);
}
.btn-ghost:hover { background: rgba(255,255,255,0.18); color: white; }

/* Visual Cards */
.hero-visual {
  display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;
  padding: 0 40px;
  position: relative; z-index: 10;
}
.visual-card {
  display: flex; align-items: center; gap: 14px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.15);
  backdrop-filter: blur(16px);
  border-radius: 14px;
  padding: 16px 22px;
  color: white;
  animation: slideUp 0.6s ease both;
}
.visual-card.vc-2 { animation-delay: 0.1s; }
.visual-card.vc-3 { animation-delay: 0.2s; }
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.visual-card i { font-size: 1.6rem; color: #5bc4ff; }
.visual-card div { display: flex; flex-direction: column; }
.visual-card strong { font-size: 0.9rem; font-weight: 700; }
.visual-card span { font-size: 0.78rem; opacity: 0.7; }

/* ── Roles Section ── */
.roles-section, .features-section {
  padding: 80px 60px;
  background: #f8faff;
}
.features-section { background: white; }

.section-header { text-align: center; margin-bottom: 52px; }
.section-header h2 { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 10px; }
.section-header p { color: #64748b; font-size: 1rem; }

.roles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; max-width: 1100px; margin: 0 auto; }

.role-card {
  background: white;
  border-radius: 20px;
  padding: 36px 28px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.role-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 4px;
}
.role-doctor::before { background: linear-gradient(90deg, #1a6fc4, #0ea5e9); }
.role-secretary::before { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.role-patient::before { background: linear-gradient(90deg, #059669, #06d6a0); }

.role-card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(0,0,0,0.1); }

.role-icon {
  width: 56px; height: 56px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 20px;
}
.role-doctor .role-icon { background: #eff6ff; color: #1a6fc4; }
.role-secretary .role-icon { background: #f5f3ff; color: #7c3aed; }
.role-patient .role-icon { background: #ecfdf5; color: #059669; }

.role-card h3 { font-size: 1.25rem; font-weight: 800; margin-bottom: 8px; }
.role-card > p { color: #64748b; font-size: 0.9rem; margin-bottom: 18px; }
.role-card ul { list-style: none; padding: 0; margin-bottom: 24px; }
.role-card ul li { display: flex; align-items: center; gap: 8px; font-size: 0.88rem; color: #475569; padding: 4px 0; }
.role-card ul li i { color: #10b981; font-size: 0.85rem; }

.role-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.88rem; font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}
.role-doctor .role-btn { background: #eff6ff; color: #1a6fc4; }
.role-secretary .role-btn { background: #f5f3ff; color: #7c3aed; }
.role-patient .role-btn { background: #ecfdf5; color: #059669; }
.role-btn:hover { opacity: 0.85; transform: translateX(3px); }

/* ── Features ── */
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; max-width: 1100px; margin: 0 auto; }
.feature-item { padding: 28px; border-radius: 14px; border: 1px solid #e2e8f0; transition: all 0.2s; }
.feature-item:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.07); transform: translateY(-2px); }
.feature-icon { width: 48px; height: 48px; background: #eff6ff; color: #1a6fc4; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 14px; }
.feature-item h4 { font-size: 1rem; font-weight: 700; margin-bottom: 6px; }
.feature-item p { color: #64748b; font-size: 0.88rem; }

/* ── Footer ── */
.landing-footer { background: #0d1b2e; color: rgba(255,255,255,0.6); text-align: center; padding: 32px 40px; }
.footer-brand { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 10px; color: white; font-weight: 700; font-size: 1.1rem; }
.footer-brand .brand-icon { background: rgba(255,255,255,0.1); }
.landing-footer p { font-size: 0.85rem; }

@media (max-width: 768px) {
  .landing-nav { padding: 20px 24px; }
  .hero-content { padding: 40px 24px 32px; }
  .roles-section, .features-section { padding: 60px 24px; }
}
</style>
