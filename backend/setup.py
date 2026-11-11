"""
DentalCare — Script de configuration Python (multi-plateforme)
Compatible Windows, Linux, macOS

Exécuter : python setup.py
"""
import os
import sys
import subprocess


def run(cmd, **kwargs):
    print(f"  → {cmd}")
    result = subprocess.run(cmd, shell=True, **kwargs)
    if result.returncode != 0:
        print(f"  ⚠️  Erreur (code {result.returncode})")
    return result


def main():
    print("=" * 60)
    print("  🦷 DentalCare — Configuration Django")
    print("=" * 60)
    print()

    # ── 1. Installation dépendances ──
    print("📦 Installation des dépendances Python...")
    run(f"{sys.executable} -m pip install -r requirements.txt")

    # ── 2. Migrations ──
    print("\n📊 Création des migrations...")
    run(f"{sys.executable} manage.py makemigrations")

    print("\n📊 Application des migrations (création de la base SQLite)...")
    run(f"{sys.executable} manage.py migrate")

    # ── Note sur la base de données ──
    print("\n" + "─" * 60)
    print("  📁 BASE DE DONNÉES")
    print("─" * 60)
    print("  Type     : SQLite (par défaut)")
    print("  Fichier  : backend/db.sqlite3")
    print("  Toutes les données sont stockées dans CE SEUL FICHIER.")
    print("  Il est créé automatiquement par 'migrate'.")
    print()
    print("  Tables créées :")
    print("   • users              → comptes (médecin, secrétaire, patient)")
    print("   • doctor_profiles    → spécialisation, licence, bio")
    print("   • patient_profiles   → date naissance, groupe sanguin, etc.")
    print("   • appointments       → rendez-vous (date, heure, statut)")
    print("   • prescriptions      → médicaments prescrits")
    print("   • medical_notes      → notes/conseils/diagnostic")
    print("   • token_blacklist_*  → tokens JWT invalidés (logout)")
    print()
    print("  Pour utiliser PostgreSQL à la place → voir README.md")
    print("─" * 60)

    # ── 3. Données démo ──
    print("\n👤 Création des comptes de démonstration...")

    demo_script = """
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dental_backend.settings')
django.setup()

from api.models import User, DoctorProfile, PatientProfile, Appointment
import datetime

def create_user(email, password, first, last, role, phone=''):
    if not User.objects.filter(email=email).exists():
        u = User.objects.create_user(
            email=email, password=password,
            first_name=first, last_name=last,
            role=role, phone=phone
        )
        print(f'  ✅ {role.capitalize()} créé : {email} / {password}')
        return u
    else:
        print(f'  ℹ️  {email} existe déjà')
        return User.objects.get(email=email)

# Superadmin
if not User.objects.filter(email='admin@dentalcare.com').exists():
    User.objects.create_superuser(
        email='admin@dentalcare.com', password='admin123',
        first_name='Admin', last_name='System'
    )
    print('  ✅ Admin créé : admin@dentalcare.com / admin123')

# Médecin
doc = create_user('doctor@dentalcare.com', 'doctor123', 'Sarah', 'Mitchell', 'doctor', '+33 6 01 02 03 04')
if not hasattr(doc, 'doctor_profile'):
    DoctorProfile.objects.get_or_create(
        user=doc,
        defaults={
            'specialization': 'Dentisterie Générale & Orthodontie',
            'license_number': 'DR-78423',
            'years_of_experience': 12,
            'bio': 'Dr. Mitchell est dentiste avec 12 ans d\\'expérience.',
            'working_hours_start': '09:00',
            'working_hours_end': '18:00',
        }
    )

# Secrétaire
create_user('secretary@dentalcare.com', 'secretary123', 'Emma', 'Johnson', 'secretary', '+33 6 05 06 07 08')

# Patient
pat = create_user('patient@dentalcare.com', 'patient123', 'James', 'Wilson', 'patient', '+33 6 09 10 11 12')
if not hasattr(pat, 'patient_profile'):
    PatientProfile.objects.get_or_create(
        user=pat,
        defaults={
            'date_of_birth': '1990-05-15',
            'gender': 'M',
            'blood_type': 'A+',
            'address': '12 Rue de la Paix, Paris 75001',
            'emergency_contact': 'Marie Wilson',
            'emergency_phone': '+33 6 99 88 77 66',
            'insurance_number': 'INS-45678',
            'allergies': 'Pénicilline',
        }
    )

# Rendez-vous de démo
doc = User.objects.filter(email='doctor@dentalcare.com').first()
pat = User.objects.filter(email='patient@dentalcare.com').first()
if doc and pat and not Appointment.objects.exists():
    today = datetime.date.today()
    Appointment.objects.create(
        patient=pat, doctor=doc, created_by=doc,
        date=today, time='10:00:00',
        treatment_type='checkup', status='confirmed',
        reason='Bilan dentaire annuel + détartrage',
        duration_minutes=45
    )
    Appointment.objects.create(
        patient=pat, doctor=doc, created_by=doc,
        date=today, time='14:30:00',
        treatment_type='cleaning', status='pending',
        reason='Nettoyage et polissage',
        duration_minutes=30
    )
    print('  ✅ 2 rendez-vous de démonstration créés pour aujourd\\'hui')

print()
print('  Données insérées dans : backend/db.sqlite3')
"""

    with open('_demo_data.py', 'w', encoding='utf-8') as f:
        f.write(demo_script)

    run(f"{sys.executable} _demo_data.py")
    os.remove('_demo_data.py')

    print()
    print("=" * 60)
    print("  ✅ Configuration terminée !")
    print("=" * 60)
    print()
    print("  Comptes de démonstration :")
    print("  🔑 Admin     : admin@dentalcare.com     / admin123")
    print("  👨‍⚕️ Médecin   : doctor@dentalcare.com    / doctor123")
    print("  👩‍💼 Secrétaire: secretary@dentalcare.com  / secretary123")
    print("  🧑‍🦱 Patient   : patient@dentalcare.com   / patient123")
    print()
    print("  Démarrer le serveur : python manage.py runserver")
    print("  Admin Django       : http://localhost:8000/admin/")
    print("  API                : http://localhost:8000/api/")
    print()
    print("  Base de données    : backend/db.sqlite3  (fichier local)")
    print("=" * 60)


if __name__ == '__main__':
    main()
