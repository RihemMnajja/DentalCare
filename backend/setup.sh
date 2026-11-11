#!/bin/bash
# DentalCare Backend Setup Script

echo "=========================================="
echo "  DentalCare Backend Setup (Django)"
echo "=========================================="

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "📊 Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating admin superuser..."
python manage.py shell -c "
from api.models import User
if not User.objects.filter(email='admin@dentalcare.com').exists():
    User.objects.create_superuser(
        email='admin@dentalcare.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created: admin@dentalcare.com / admin123')
else:
    print('ℹ️  Superuser already exists')
"

# Create demo data
echo "🦷 Creating demo users and data..."
python manage.py shell -c "
from api.models import User, DoctorProfile, PatientProfile, Appointment
import datetime

# Doctor
if not User.objects.filter(email='doctor@dentalcare.com').exists():
    doc = User.objects.create_user(
        email='doctor@dentalcare.com',
        password='doctor123',
        first_name='Sarah',
        last_name='Mitchell',
        role='doctor',
        phone='+1 555 0101'
    )
    DoctorProfile.objects.create(
        user=doc,
        specialization='General Dentistry & Orthodontics',
        license_number='DR-78423',
        years_of_experience=12,
        bio='Dr. Mitchell is a dedicated dental professional with over 12 years of experience.'
    )
    print('✅ Doctor created: doctor@dentalcare.com / doctor123')

# Secretary
if not User.objects.filter(email='secretary@dentalcare.com').exists():
    User.objects.create_user(
        email='secretary@dentalcare.com',
        password='secretary123',
        first_name='Emma',
        last_name='Johnson',
        role='secretary',
        phone='+1 555 0102'
    )
    print('✅ Secretary created: secretary@dentalcare.com / secretary123')

# Patient
if not User.objects.filter(email='patient@dentalcare.com').exists():
    pat = User.objects.create_user(
        email='patient@dentalcare.com',
        password='patient123',
        first_name='James',
        last_name='Wilson',
        role='patient',
        phone='+1 555 0103'
    )
    PatientProfile.objects.create(
        user=pat,
        date_of_birth='1990-05-15',
        gender='M',
        blood_type='A+',
        address='123 Main Street, New York, NY',
        emergency_contact='Mary Wilson',
        emergency_phone='+1 555 0199',
        insurance_number='INS-45678'
    )
    print('✅ Patient created: patient@dentalcare.com / patient123')

# Sample appointment
doc = User.objects.filter(email='doctor@dentalcare.com').first()
pat = User.objects.filter(email='patient@dentalcare.com').first()
if doc and pat and not Appointment.objects.exists():
    today = datetime.date.today()
    Appointment.objects.create(
        patient=pat, doctor=doc, created_by=doc,
        date=today, time='10:00:00',
        treatment_type='checkup', status='confirmed',
        reason='Regular dental checkup and cleaning'
    )
    print('✅ Sample appointment created for today')
"

echo ""
echo "=========================================="
echo "  ✅ Backend setup complete!"
echo "=========================================="
echo ""
echo "  Demo accounts:"
echo "  🔑 Admin:     admin@dentalcare.com / admin123"
echo "  👨‍⚕️ Doctor:    doctor@dentalcare.com / doctor123"
echo "  👩‍💼 Secretary: secretary@dentalcare.com / secretary123"
echo "  🧑‍🦱 Patient:   patient@dentalcare.com / patient123"
echo ""
echo "  Start server: python manage.py runserver"
echo "=========================================="
