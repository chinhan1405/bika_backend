from rest_framework import request, views
from rest_framework.permissions import IsAuthenticated

from . import constants


class IsLecturer(IsAuthenticated):
    """Custom permission to only allow lecturers to access the view."""

    def has_permission(
        self,
        request: request.HttpRequest,
        view: views.APIView,
    ) -> bool:
        """Check if the user is authenticated and has the 'lecturer' role."""
        return super().has_permission(request, view) and (
            getattr(request.user, "role", None) == constants.UserRole.LECTURER
        )


class IsAdmin(IsAuthenticated):
    """Custom permission to only allow admins to access the view."""

    def has_permission(
        self,
        request: request.HttpRequest,
        view: views.APIView,
    ) -> bool:
        """Check if the user is authenticated and has the 'admin' role."""
        return super().has_permission(request, view) and (
            getattr(request.user, "role", None) == constants.UserRole.ADMIN
        )


class IsStudent(IsAuthenticated):
    """Custom permission to only allow students to access the view."""

    def has_permission(
        self,
        request: request.HttpRequest,
        view: views.APIView,
    ) -> bool:
        """Check if the user is authenticated and has the 'student' role."""
        return super().has_permission(request, view) and (
            getattr(request.user, "role", None) == constants.UserRole.STUDENT
        )
