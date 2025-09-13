# taches/views/commentaire_view.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.contrib.contenttypes.models import ContentType

from taches.models.commentaire_model import Commentaire
from taches.serializers.commentaire_serializer import CommentaireSerializer


@extend_schema(tags=["Commentaires"])
class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtre les commentaires selon :
        - content_type & object_id : pour cibler un objet spécifique
        - parent : pour récupérer les réponses ou uniquement les commentaires racine
        - include_deleted : inclure les commentaires supprimés si demandé
        """
        queryset = super().get_queryset()
        params = self.request.query_params

        content_type = params.get("content_type")
        object_id = params.get("object_id")
        include_deleted = params.get("include_deleted", "false").lower() == "true"
        parent = params.get("parent")

        if content_type and object_id:
            try:
                ct = ContentType.objects.get(model=content_type.lower())
                queryset = queryset.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                return Commentaire.objects.none()

        if parent is not None:
            queryset = queryset.filter(parent_id=parent)
        else:
            queryset = queryset.filter(parent__isnull=True)

        if not include_deleted:
            queryset = queryset.filter(is_deleted=False)

        return queryset.order_by("date_creation")

    @extend_schema(
        description="Créer un commentaire sur une tâche ou un autre objet",
        request=CommentaireSerializer,
        responses={201: CommentaireSerializer},
        examples=[
            OpenApiExample(
                "Créer un commentaire",
                value={
                    "contenu": "Super tâche !",
                    "cible_type": "tache",
                    "cible_id": 7,
                    "parent": None
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        cible_type = data.pop("cible_type", None)
        cible_id = data.pop("cible_id", None)
        parent_id = data.get("parent")

        if not cible_type or not cible_id:
            return Response(
                {"detail": "cible_type et cible_id obligatoires"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ct = ContentType.objects.get(model=cible_type.lower())
        except ContentType.DoesNotExist:
            return Response(
                {"detail": f"ContentType '{cible_type}' non trouvé"},
                status=status.HTTP_400_BAD_REQUEST
            )

        commentaire = Commentaire.objects.create(
            auteur=request.user,
            contenu=data.get("contenu", ""),
            content_type=ct,
            object_id=cible_id,
            parent_id=parent_id,
        )
        serializer = self.get_serializer(commentaire)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
