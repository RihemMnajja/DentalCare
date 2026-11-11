# 🦷 DentalCare Appointment Management System

Stack : **Django REST Framework** + **Vue.js 3** + **Bootstrap 5**

---

## 📁 Structure du projet

```
dental-system/
├── backend/                    ← API Django
│   ├── dental_backend/         ← Settings, URLs, WSGI
│   ├── api/                    ← App principale
│   │   ├── models.py           ← Modèles de données
│   │   ├── serializers.py      ← Sérialiseurs DRF
│   │   ├── views.py            ← Vues API + ViewSets
│   │   ├── urls.py             ← Routes API
│   │   ├── permissions.py      ← Permissions par rôle
│   │   ├── apps.py             ← Configuration de l'app
│   │   └── migrations/         ← Migrations SQLite
│   ├── manage.py
│   ├── requirements.txt
│   ├── setup.py                ← Script de config (multi-plateforme)
│   └── setup.sh                ← Script Bash (Linux/Mac)
│
└── frontend/                   ← SPA Vue.js 3
    ├── src/
    │   ├── api/axios.js         ← Client HTTP + auto-refresh JWT
    │   ├── assets/styles/       ← CSS global
    │   ├── components/          ← AppSidebar, AppHeader
    │   ├── router/              ← Vue Router + guards
    │   ├── stores/              ← Pinia (auth, appointments)
    │   └── views/
    │       ├── LandingPage.vue
    │       ├── auth/            ← Login, Register
    │       ├── doctor/          ← Dashboard, Appointments, Patients, Prescriptions, Profile
    │       ├── secretary/       ← Dashboard, Appointments, Calendar, Patients, Profile
    │       └── patient/         ← Dashboard, Appointments, Prescriptions, Notes, Profile
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## 🗄️ BASE DE DONNÉES — Explication complète

### Par défaut : SQLite

```
backend/db.sqlite3   ← UN SEUL FICHIER binaire
```

**C'est quoi SQLite ?**
SQLite est une base de données embarquée (pas de serveur). Toutes vos données
sont stockées dans le fichier `db.sqlite3`. Ce fichier est créé automatiquement
par la commande `python manage.py migrate`.

**Avantages :** Aucune installation, parfait pour le développement et les démos.
**Inconvénients :** Pas adapté pour plusieurs serveurs en parallèle (production).

### Tables créées par `migrate`

| Table | Contenu |
|-------|---------|
| `users` | Tous les comptes (médecin, secrétaire, patient, admin) |
| `doctor_profiles` | Spécialisation, licence, bio, horaires |
| `patient_profiles` | Date naissance, groupe sanguin, allergies, assurance |
| `appointments` | Rendez-vous : date, heure, durée, type, statut |
| `prescriptions` | Médicaments : nom, dosage, fréquence, durée |
| `medical_notes` | Notes/diagnostics/conseils des médecins |
| `token_blacklist_blacklistedtoken` | Tokens JWT révoqués (logout) |
| `token_blacklist_outstandingtoken` | Tokens JWT actifs |
| `django_admin_log` | Journal de l'admin Django |
| `auth_permission / auth_group` | Permissions Django standard |

### Comment voir les données ?

**Option 1 — Admin Django (recommandé)**
```
http://localhost:8000/admin/
Compte : admin@dentalcare.com / admin123
```

**Option 2 — DB Browser for SQLite** (application gratuite)
Téléchargez : https://sqlitebrowser.org/
Ouvrir le fichier `backend/db.sqlite3`

**Option 3 — Ligne de commande**
```bash
cd backend
python manage.py shell
>>> from api.models import User, Appointment
>>> User.objects.all()
>>> Appointment.objects.filter(status='confirmed')
```

**Option 4 — API REST**
```
GET http://localhost:8000/api/appointments/
GET http://localhost:8000/api/patients/
```

### Passer à PostgreSQL (production)

1. Installez PostgreSQL et créez une base :
```sql
CREATE DATABASE dentalcare_db;
CREATE USER dental_user WITH PASSWORD 'votre_mdp';
GRANT ALL PRIVILEGES ON DATABASE dentalcare_db TO dental_user;
```

2. Installez le driver Python :
```bash
pip install psycopg2-binary
```

3. Modifiez `backend/dental_backend/settings.py` :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dentalcare_db',
        'USER': 'dental_user',
        'PASSWORD': 'votre_mdp',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Relancez les migrations :
```bash
python manage.py migrate
python setup.py    # recrée les données démo
```

### Passer à MySQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dentalcare_db',
        'USER': 'dental_user',
        'PASSWORD': 'votre_mdp',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
```bash
pip install mysqlclient
python manage.py migrate
```

---

## 🚀 Démarrage rapide

### Prérequis
- Python 3.10+
- Node.js 18+

### Backend

```bash
cd dental-system/backend

# 1. Environnement virtuel
python3 -m venv venv
source venv/bin/activate     # Linux/Mac
# OU
venv\Scripts\activate         # Windows

# 2. Configuration automatique
python setup.py
# → installe pip, crée db.sqlite3, insère données démo

# 3. Démarrer le serveur
python manage.py runserver
# API : http://localhost:8000/api/
# Admin : http://localhost:8000/admin/
```

### Frontend

```bash
cd dental-system/frontend

npm install
npm run dev
# → http://localhost:5173
```

---

## 👤 Comptes de démonstration

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Admin | admin@dentalcare.com | admin123 |
| Médecin | doctor@dentalcare.com | doctor123 |
| Secrétaire | secretary@dentalcare.com | secretary123 |
| Patient | patient@dentalcare.com | patient123 |

---

## 🔐 Authentification JWT

```
POST /api/auth/login/    → retourne access (24h) + refresh (7j)
POST /api/auth/refresh/  → renouvelle access avec refresh
POST /api/auth/logout/   → blacklist le refresh token
```

Le frontend stocke les tokens dans `localStorage` et les attache automatiquement
à chaque requête via un intercepteur Axios.

---

## 📡 API Endpoints principaux

```
GET/POST   /api/appointments/
GET/PATCH  /api/appointments/{id}/
PATCH      /api/appointments/{id}/update_status/   ← changer statut
GET        /api/appointments/statistics/            ← stats tableau de bord

GET/POST   /api/prescriptions/     ← POST réservé au médecin
GET/POST   /api/notes/             ← POST réservé au médecin

GET        /api/patients/          ← médecin + secrétaire seulement
GET        /api/doctors/
GET        /api/dashboard/         ← données du tableau de bord par rôle
GET/PATCH  /api/profile/           ← profil de l'utilisateur connecté
```

---

## 🐛 Bugs corrigés dans cette version

| # | Fichier | Problème | Correction |
|---|---------|----------|------------|
| 1 | `api/apps.py` | Fichier manquant | Créé — Django enregistre correctement l'app |
| 2 | `api/migrations/` | Dossier manquant | Créé — `makemigrations` fonctionne |
| 3 | `serializers.py` | Champ `doctor` requis → HTTP 400 sur toutes tâches docteur | `doctor` mis en `read_only_fields` |
| 4 | `AppHeader.vue` | Lien profil hardcodé `/patient/profile` | Route dynamique `/${auth.userRole}/profile` |
| 5 | `router/index.js` | Routes `/doctor/profile` et `/secretary/profile` manquantes | Ajoutées avec leurs composants |
| 6 | `setup.sh` | Ne fonctionne pas sur Windows | Script `setup.py` Python alternatif créé |

---

## 🛠 Stack technique complète

| Couche | Technologie | Version |
|--------|-------------|---------|
| Backend | Django | 4.2 |
| API REST | Django REST Framework | 3.14 |
| Auth | SimpleJWT | 5.3 |
| CORS | django-cors-headers | 4.3 |
| Filtres | django-filter | 23.3 |
| Base de données | SQLite (dev) / PostgreSQL (prod) | — |
| Frontend | Vue.js 3 (Composition API) | 3.4 |
| État | Pinia | 2.1 |
| Router | Vue Router | 4.2 |
| UI | Bootstrap 5 + Bootstrap Icons | 5.3 |
| Build | Vite | 5.0 |
| HTTP | Axios | 1.6 |
| Dates | date-fns | 3.0 |
| Toasts | vue-toastification | 2.0 |
"# DentalCare" 
