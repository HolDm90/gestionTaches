# taches/permissions.py
from rest_framework.permissions import BasePermission

class IsValidatedUser(BasePermission):
    """
    Autorise uniquement les utilisateurs validés.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_validated

class IsMembre(BasePermission):
    """
    Autorise uniquement les utilisateurs validés dans le groupe 'Membre'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_validated and request.user.has_group("Membre")

class IsChefEquipe(BasePermission):
    """
    Autorise uniquement les utilisateurs validés dans le groupe 'Chef d’équipe'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_validated and request.user.has_group("Chef d’équipe")
