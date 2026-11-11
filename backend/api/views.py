from django.utils import timezone
from django.db.models import Q
from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_filters.rest_framework import DjangoFilterBackend
import datetime

from .models import User, Appointment, Prescription, MedicalNote, DoctorProfile, PatientProfile
from .serializers import (
    UserSerializer, RegisterSerializer, AppointmentSerializer,
    PrescriptionSerializer, MedicalNoteSerializer, UserMiniSerializer,
    DoctorProfileSerializer, PatientProfileSerializer
)
from .permissions import IsDoctor, IsSecretary, IsPatient, IsDoctorOrSecretary, IsOwnerOrStaff


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'phone': user.phone,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DoctorListView(generics.ListAPIView):
    serializer_class = UserMiniSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role='doctor', is_active=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']


class PatientListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsDoctorOrSecretary]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email', 'phone']

    def get_queryset(self):
        return User.objects.filter(role='patient', is_active=True)


class PatientDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ['doctor', 'secretary', 'admin']:
            return User.objects.filter(role='patient')
        return User.objects.filter(id=self.request.user.id)


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'treatment_type', 'doctor', 'patient', 'date']
    search_fields = ['patient__first_name', 'patient__last_name', 'reason', 'notes']
    ordering_fields = ['date', 'time', 'created_at', 'status']
    ordering = ['date', 'time']

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.select_related('patient', 'doctor').all()
        if user.role == 'doctor':
            qs = qs.filter(doctor=user)
        elif user.role == 'patient':
            qs = qs.filter(patient=user)
        # Secretary and admin see all

        # Date filtering
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        today = self.request.query_params.get('today')
        if today:
            qs = qs.filter(date=timezone.now().date())

        upcoming = self.request.query_params.get('upcoming')
        if upcoming:
            qs = qs.filter(date__gte=timezone.now().date(), status__in=['pending', 'confirmed'])

        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsDoctorOrSecretary])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = [s[0] for s in Appointment.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        appointment.status = new_status
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        user = request.user
        today = timezone.now().date()
        qs = Appointment.objects.all()
        if user.role == 'doctor':
            qs = qs.filter(doctor=user)
        elif user.role == 'patient':
            qs = qs.filter(patient=user)

        stats = {
            'total': qs.count(),
            'today': qs.filter(date=today).count(),
            'upcoming': qs.filter(date__gte=today, status__in=['pending', 'confirmed']).count(),
            'completed': qs.filter(status='completed').count(),
            'cancelled': qs.filter(status='cancelled').count(),
            'pending': qs.filter(status='pending').count(),
            'confirmed': qs.filter(status='confirmed').count(),
        }
        return Response(stats)


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'is_active']
    search_fields = ['medication_name', 'patient__first_name', 'patient__last_name']
    ordering = ['-date_issued']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Prescription.objects.filter(doctor=user)
        elif user.role == 'patient':
            return Prescription.objects.filter(patient=user)
        return Prescription.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDoctor()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class MedicalNoteViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'note_type']
    search_fields = ['title', 'content', 'patient__first_name', 'patient__last_name']
    ordering = ['-date_created']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalNote.objects.filter(doctor=user)
        elif user.role == 'patient':
            return MedicalNote.objects.filter(patient=user, is_private=False)
        return MedicalNote.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDoctor()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        if user.role == 'doctor':
            appointments_today = Appointment.objects.filter(
                doctor=user, date=today
            ).select_related('patient').order_by('time')
            upcoming = Appointment.objects.filter(
                doctor=user, date__gt=today, status__in=['pending', 'confirmed']
            ).count()
            total_patients = Appointment.objects.filter(
                doctor=user
            ).values('patient').distinct().count()
            recent_prescriptions = Prescription.objects.filter(
                doctor=user
            ).order_by('-date_issued')[:5]

            return Response({
                'appointments_today': AppointmentSerializer(appointments_today, many=True).data,
                'appointments_today_count': appointments_today.count(),
                'upcoming_count': upcoming,
                'total_patients': total_patients,
                'recent_prescriptions': PrescriptionSerializer(recent_prescriptions, many=True).data,
            })

        elif user.role == 'secretary':
            appointments_today = Appointment.objects.filter(
                date=today
            ).select_related('patient', 'doctor').order_by('time')
            upcoming = Appointment.objects.filter(
                date__gt=today, status__in=['pending', 'confirmed']
            ).count()
            total_patients = User.objects.filter(role='patient').count()
            pending = Appointment.objects.filter(status='pending').count()

            return Response({
                'appointments_today': AppointmentSerializer(appointments_today, many=True).data,
                'appointments_today_count': appointments_today.count(),
                'upcoming_count': upcoming,
                'total_patients': total_patients,
                'pending_count': pending,
            })

        elif user.role == 'patient':
            upcoming = Appointment.objects.filter(
                patient=user, date__gte=today, status__in=['pending', 'confirmed']
            ).select_related('doctor').order_by('date', 'time')
            past = Appointment.objects.filter(
                patient=user, status='completed'
            ).select_related('doctor').order_by('-date')[:5]
            prescriptions = Prescription.objects.filter(
                patient=user, is_active=True
            ).order_by('-date_issued')
            notes = MedicalNote.objects.filter(
                patient=user, is_private=False
            ).order_by('-date_created')[:5]

            return Response({
                'upcoming_appointments': AppointmentSerializer(upcoming, many=True).data,
                'upcoming_count': upcoming.count(),
                'past_appointments': AppointmentSerializer(past, many=True).data,
                'total_completed': Appointment.objects.filter(patient=user, status='completed').count(),
                'prescriptions': PrescriptionSerializer(prescriptions, many=True).data,
                'medical_notes': MedicalNoteSerializer(notes, many=True).data,
            })

        return Response({'detail': 'Unknown role'}, status=400)
