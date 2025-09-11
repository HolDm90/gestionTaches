from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied

from taches.models.statut_model import Statut
from taches.serializers.statut_serializer import StatutSerializer
from taches.permissions import IsChefEquipe, IsValidatedUser

@extend_schema(tags=["Statuts"])
class StatutViewSet(viewsets.ModelViewSet):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer

    def get_permissions(self):
        user = self.request.user  # ⚠️ Toujours récupérer l'utilisateur en premier

        # Vérifie que l'utilisateur est authentifié
        if not user.is_authenticated:
            return [IsAuthenticated()]

        if self.action in ["create", "update", "partial_update", "destroy"]:
            # Seul le chef d'équipe peut gérer les statuts
            if user.has_group("Chef d’équipe"):
                return [IsAuthenticated(), IsChefEquipe()]
            else:
                # Membres et admin → lecture seule
                return [IsAuthenticated()]

        # Lecture accessible aux utilisateurs validés
        return [IsAuthenticated(), IsValidatedUser()]

    def perform_update(self, serializer):
        user = self.request.user
        if user.has_group("Chef d’équipe"):
            serializer.save()  # Chef peut tout modifier
        else:
            raise PermissionDenied("Seul le chef d’équipe peut modifier un statut.")
