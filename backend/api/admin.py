from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DoctorProfile, PatientProfile, Appointment, Prescription, MedicalNote


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.role == 'doctor':
                return [DoctorProfileInline]
            elif obj.role == 'patient':
                return [PatientProfileInline]
        return []


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'treatment_type', 'status']
    list_filter = ['status', 'treatment_type', 'date']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__last_name']
    date_hierarchy = 'date'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication_name', 'patient', 'doctor', 'date_issued', 'is_active']
    list_filter = ['is_active', 'date_issued']
    search_fields = ['medication_name', 'patient__first_name', 'patient__last_name']


@admin.register(MedicalNote)
class MedicalNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'note_type', 'patient', 'doctor', 'date_created']
    list_filter = ['note_type', 'is_private']
    search_fields = ['title', 'patient__first_name', 'patient__last_name']
