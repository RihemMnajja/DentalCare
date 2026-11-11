from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, DoctorProfile, PatientProfile, Appointment, Prescription, MedicalNote


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'license_number', 'bio', 'years_of_experience',
                  'working_hours_start', 'working_hours_end']


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'address', 'emergency_contact',
                  'emergency_phone', 'blood_type', 'allergies', 'medical_history', 'insurance_number']


class UserSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(read_only=True)
    patient_profile = PatientProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'role',
                  'phone', 'avatar', 'date_joined', 'doctor_profile', 'patient_profile']
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.full_name


class UserMiniSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'phone']

    def get_full_name(self, obj):
        return obj.full_name


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    doctor_profile = DoctorProfileSerializer(required=False)
    patient_profile = PatientProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2',
                  'role', 'phone', 'doctor_profile', 'patient_profile']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor_profile', None)
        patient_data = validated_data.pop('patient_profile', None)
        validated_data.pop('password2')

        user = User.objects.create_user(**validated_data)

        if user.role == 'doctor':
            DoctorProfile.objects.create(user=user, **(doctor_data or {}))
        elif user.role == 'patient':
            PatientProfile.objects.create(user=user, **(patient_data or {}))

        return user


class AppointmentSerializer(serializers.ModelSerializer):
    patient_detail = UserMiniSerializer(source='patient', read_only=True)
    doctor_detail = UserMiniSerializer(source='doctor', read_only=True)
    prescriptions_count = serializers.SerializerMethodField()
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'patient_detail', 'doctor_detail',
                  'date', 'time', 'duration_minutes', 'treatment_type', 'status',
                  'reason', 'notes', 'created_at', 'updated_at',
                  'prescriptions_count', 'notes_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_prescriptions_count(self, obj):
        return obj.prescriptions.count()

    def get_notes_count(self, obj):
        return obj.medical_notes.count()


class PrescriptionSerializer(serializers.ModelSerializer):
    patient_detail = UserMiniSerializer(source='patient', read_only=True)
    doctor_detail = UserMiniSerializer(source='doctor', read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'patient', 'doctor', 'patient_detail', 'doctor_detail',
                  'medication_name', 'dosage', 'frequency', 'duration',
                  'instructions', 'date_issued', 'is_active']
        # BUG FIX: 'doctor' est read_only.
        # Le frontend ne l'envoie PAS dans le body.
        # perform_create() l'injecte via serializer.save(doctor=request.user).
        # Sans ce fix : Django retournait HTTP 400 "This field is required."
        read_only_fields = ['id', 'date_issued', 'doctor']


class MedicalNoteSerializer(serializers.ModelSerializer):
    patient_detail = UserMiniSerializer(source='patient', read_only=True)
    doctor_detail = UserMiniSerializer(source='doctor', read_only=True)

    class Meta:
        model = MedicalNote
        fields = ['id', 'appointment', 'patient', 'doctor', 'patient_detail', 'doctor_detail',
                  'note_type', 'title', 'content', 'date_created', 'is_private']
        # BUG FIX: même raison que PrescriptionSerializer ci-dessus.
        read_only_fields = ['id', 'date_created', 'doctor']
