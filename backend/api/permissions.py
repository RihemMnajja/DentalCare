from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'


class IsSecretary(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'secretary'


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'


class IsDoctorOrSecretary(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['doctor', 'secretary', 'admin']


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['doctor', 'secretary', 'admin']:
            return True
        if hasattr(obj, 'patient'):
            return obj.patient == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
