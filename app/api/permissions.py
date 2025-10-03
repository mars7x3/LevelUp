from rest_framework.permissions import BasePermission

from db.enums import StaffRole


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.DIRECTOR


class IsReceiver(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.RECEIVER

