from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
router.register(r'notes', views.MedicalNoteViewSet, basename='note')

urlpatterns = [
    # Auth
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Users
    path('doctors/', views.DoctorListView.as_view(), name='doctors-list'),
    path('patients/', views.PatientListView.as_view(), name='patients-list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),

    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # ViewSets
    path('', include(router.urls)),
]
