from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from taches.models.tache_model import Tache
from taches.models.team_model import Team
from taches.models.team_member_model import TeamMembers
from taches.models.statut_model import Statut
from taches.models.priorite_model import Priorite
from taches.serializers.tache_serializer import TacheSerializer
from taches.permissions import IsChefEquipe, IsMembre, IsValidatedUser


class AssignTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()


@extend_schema(tags=["Tâches"])
class TacheViewSet(viewsets.ModelViewSet):
    queryset = Tache.objects.select_related("equipe", "statut", "priorite").prefetch_related("commentaires")
    serializer_class = TacheSerializer

    def get_permissions(self):
        user = self.request.user

        # ⚠️ Toujours vérifier que l'utilisateur est authentifié
        if not user.is_authenticated:
            return [IsAuthenticated()]

        if self.action in ["create", "update", "partial_update", "destroy", "assign_team"]:
            if hasattr(user, "has_group") and user.has_group("Chef d’équipe"):
                return [IsAuthenticated(), IsChefEquipe()]
            elif hasattr(user, "has_group") and user.has_group("Membre"):
                return [IsAuthenticated(), IsMembre()]
            else:
                # Admin → lecture seule
                return [IsAuthenticated()]
        
        # Lecture pour tous les utilisateurs validés
        return [IsAuthenticated(), IsValidatedUser()]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Tache.objects.none()

        if hasattr(user, "has_group") and user.has_group("Chef d’équipe"):
            return Tache.objects.filter(equipe__teammembers__user=user).distinct()
        elif hasattr(user, "has_group") and user.has_group("Membre"):
            return Tache.objects.filter(equipe__teammembers__user=user).distinct()
        elif user.is_superuser:
            return Tache.objects.all()
        return Tache.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not (hasattr(user, "has_group") and user.has_group("Chef d’équipe")):
            raise PermissionDenied("Seul un chef d’équipe peut créer des tâches.")

        equipe = serializer.validated_data.get("equipe")
        if not equipe or not TeamMembers.objects.filter(team=equipe, user=user).exists():
            raise PermissionDenied("Vous ne pouvez créer une tâche que pour vos équipes.")

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if hasattr(user, "has_group") and user.has_group("Chef d’équipe"):
            serializer.save()
        elif hasattr(user, "has_group") and user.has_group("Membre"):
            statut = serializer.validated_data.get("statut")
            if statut:
                serializer.instance.statut = statut
                serializer.instance.save(update_fields=["statut"])
            else:
                raise PermissionDenied("Vous ne pouvez modifier que le statut de la tâche.")
        else:
            raise PermissionDenied("Lecture seule pour l'admin ou non autorisé.")

    @extend_schema(
        description="Assigner une tâche à une équipe (chef uniquement)",
        request=AssignTeamSerializer,
        responses={200: TacheSerializer}
    )
    @action(detail=True, methods=["post"], url_path="assign-team")
    def assign_team(self, request, pk=None):
        user = request.user
        if not (hasattr(user, "has_group") and user.has_group("Chef d’équipe")):
            return Response({"detail": "Accès réservé au chef d’équipe."}, status=403)

        tache = self.get_object()
        serializer = AssignTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team_id = serializer.validated_data["team_id"]
        team = Team.objects.filter(id=team_id, teammembers__user=user).first()
        if not team:
            return Response({"detail": "Équipe introuvable ou non autorisée."}, status=404)

        tache.equipe = team
        tache.save(update_fields=["equipe"])
        return Response(TacheSerializer(tache).data, status=200)

    @extend_schema(
        description="Marquer une tâche comme terminée",
        request=None,
        responses={200: {"type": "object", "example": {"detail": "Tâche marquée comme terminée."}}}
    )
    @action(detail=True, methods=["post"], url_path="mark-complete")
    def mark_complete(self, request, pk=None):
        tache = self.get_object()
        user = request.user

        if hasattr(user, "has_group") and (user.has_group("Chef d’équipe") or user.has_group("Membre")):
            if not TeamMembers.objects.filter(team=tache.equipe, user=user).exists():
                return Response({"detail": "Non autorisé."}, status=403)
        elif user.is_superuser:
            return Response({"detail": "Admin → lecture seule."}, status=403)

        tache.statut = Statut.objects.get(label="terminée")
        tache.save(update_fields=["statut"])
        return Response({"detail": "Tâche marquée comme terminée."})
