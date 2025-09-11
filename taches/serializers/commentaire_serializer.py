from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.contrib.contenttypes.models import ContentType
from taches.models.commentaire_model import Commentaire


class NestedCommentaireSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()

    class Meta:
        model = Commentaire
        fields = ["id", "auteur", "contenu", "date_creation", "is_deleted"]


class CommentaireSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()
    reponses = serializers.SerializerMethodField()
    cible_type = serializers.SerializerMethodField()
    cible_id = serializers.IntegerField(source="object_id", read_only=True)

    class Meta:
        model = Commentaire
        fields = [
            "id",
            "auteur",
            "contenu",
            "date_creation",
            "date_modification",
            "is_deleted",
            "parent",
            "reponses",
            "cible_type",
            "cible_id",
        ]

    # ✅ Type de l’objet cible (ex: "tache", "team")
    @extend_schema_field(serializers.CharField())
    def get_cible_type(self, obj):
        return obj.content_type.model if obj.content_type else None

    # ✅ Réponses imbriquées
    @extend_schema_field(NestedCommentaireSerializer(many=True))
    def get_reponses(self, obj):
        return NestedCommentaireSerializer(obj.reponses.all(), many=True).data
