"""
Permissions for the different types of users.
"""
from rest_framework import permissions


class IsOwnerOfJob(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company == request.user
