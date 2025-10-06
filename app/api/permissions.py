from rest_framework.permissions import BasePermission

from db.enums import StaffRole


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.DIRECTOR


class IsReceiver(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.RECEIVER


class IsOTK(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.OTK


class IsPacker(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.PACKER


class IsMarker(BasePermission):
    def has_permission(self, request, view):
        return request.user.staff_profile.role == StaffRole.MARKER
