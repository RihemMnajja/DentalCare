from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('secretary', 'Secretary'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=200, default='General Dentistry')
    license_number = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    years_of_experience = models.IntegerField(default=0)
    working_hours_start = models.TimeField(default='09:00')
    working_hours_end = models.TimeField(default='17:00')

    class Meta:
        db_table = 'doctor_profiles'

    def __str__(self):
        return f"Dr. {self.user.full_name}"


class PatientProfile(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'patient_profiles'

    def __str__(self):
        return f"Patient: {self.user.full_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]

    TREATMENT_CHOICES = [
        ('checkup', 'Regular Checkup'),
        ('cleaning', 'Teeth Cleaning'),
        ('filling', 'Cavity Filling'),
        ('extraction', 'Tooth Extraction'),
        ('root_canal', 'Root Canal'),
        ('crown', 'Crown/Bridge'),
        ('whitening', 'Teeth Whitening'),
        ('braces', 'Braces/Orthodontics'),
        ('implant', 'Dental Implant'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments',
                                 limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments',
                                limit_choices_to={'role': 'doctor'})
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.IntegerField(default=30)
    treatment_type = models.CharField(max_length=50, choices=TREATMENT_CHOICES, default='checkup')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['date', 'time']

    def __str__(self):
        return f"Appt: {self.patient.full_name} with Dr.{self.doctor.last_name} on {self.date}"


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions', null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions',
                                 limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_prescriptions',
                                limit_choices_to={'role': 'doctor'})
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    date_issued = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'prescriptions'
        ordering = ['-date_issued']

    def __str__(self):
        return f"{self.medication_name} for {self.patient.full_name}"


class MedicalNote(models.Model):
    NOTE_TYPE_CHOICES = [
        ('diagnosis', 'Diagnosis'),
        ('advice', 'Advice'),
        ('observation', 'Observation'),
        ('follow_up', 'Follow-up'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_notes', null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_notes',
                                 limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_notes',
                                limit_choices_to={'role': 'doctor'})
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='observation')
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        db_table = 'medical_notes'
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.note_type}: {self.title} for {self.patient.full_name}"
