from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied

from taches.models.priorite_model import Priorite
from taches.serializers.priorite_serializer import PrioriteSerializer
from taches.permissions import IsChefEquipe, IsValidatedUser

@extend_schema(tags=["Priorités"])
class PrioriteViewSet(viewsets.ModelViewSet):
    queryset = Priorite.objects.all()
    serializer_class = PrioriteSerializer

    def get_permissions(self):
        user = self.request.user

        # ⚠️ Vérifie d'abord que l'utilisateur est authentifié
        if not user.is_authenticated:
            return [IsAuthenticated()]

        # Actions de modification
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if hasattr(user, "has_group") and user.has_group("Chef d’équipe"):
                return [IsAuthenticated(), IsChefEquipe()]
            else:
                # Membres et Admin → lecture seule
                return [IsAuthenticated()]
        
        # Lecture pour les utilisateurs validés
        return [IsAuthenticated(), IsValidatedUser()]

    def perform_update(self, serializer):
        user = self.request.user
        if hasattr(user, "has_group") and user.has_group("Chef d’équipe"):
            serializer.save()  # Chef peut tout modifier
        else:
            raise PermissionDenied("Seul le chef d’équipe peut modifier une priorité.")
