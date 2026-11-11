<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Mon Profil</h1>
      <p class="page-subtitle">Gérez vos informations personnelles</p>
    </div>
    <div class="row g-4">
      <div class="col-12 col-lg-4">
        <div class="card text-center p-4">
          <div class="profile-avatar mx-auto">{{ initials }}</div>
          <h3 class="mt-3 mb-1">{{ auth.fullName }}</h3>
          <span class="role-pill">Secrétaire</span>
          <div class="profile-contact mt-3">
            <div class="contact-item"><i class="bi bi-envelope"></i> {{ auth.user?.email }}</div>
            <div v-if="auth.user?.phone" class="contact-item"><i class="bi bi-telephone"></i> {{ auth.user?.phone }}</div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-8">
        <div class="card mb-4">
          <div class="card-header">
            <span><i class="bi bi-person-gear me-2 text-primary"></i>Informations personnelles</span>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-6">
                <label class="form-label">Prénom</label>
                <input v-model="form.first_name" type="text" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">Nom</label>
                <input v-model="form.last_name" type="text" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Téléphone</label>
                <input v-model="form.phone" type="tel" class="form-control" />
              </div>
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-end gap-3">
          <button class="btn btn-outline-secondary" @click="resetForm">
            <i class="bi bi-arrow-counterclockwise me-1"></i> Réinitialiser
          </button>
          <button class="btn btn-primary" @click="save" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            <i v-else class="bi bi-check2 me-1"></i>
            {{ saving ? 'Enregistrement...' : 'Sauvegarder' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import api from '@/api/axios'

const auth = useAuthStore()
const toast = useToast()
const saving = ref(false)

const initials = computed(() => {
  const u = auth.user
  return u ? `${u.first_name?.[0]}${u.last_name?.[0]}`.toUpperCase() : '?'
})

const form = ref({ first_name: '', last_name: '', phone: '' })

function resetForm() {
  const u = auth.user
  form.value = { first_name: u?.first_name || '', last_name: u?.last_name || '', phone: u?.phone || '' }
}

async function save() {
  saving.value = true
  try {
    await api.patch('/profile/', form.value)
    await auth.fetchProfile()
    toast.success('Profil mis à jour !')
  } catch { toast.error('Erreur lors de la mise à jour.') }
  finally { saving.value = false }
}

onMounted(async () => { await auth.fetchProfile(); resetForm() })
</script>

<style scoped>
.profile-avatar { width: 80px; height: 80px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 800; }
.role-pill { background: rgba(124,58,237,0.12); color: #7c3aed; padding: 4px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
.profile-contact { display: flex; flex-direction: column; gap: 8px; text-align: left; }
.contact-item { display: flex; align-items: center; gap: 8px; font-size: 0.88rem; color: var(--text-secondary); }
.contact-item i { color: var(--primary); width: 16px; }
</style>
