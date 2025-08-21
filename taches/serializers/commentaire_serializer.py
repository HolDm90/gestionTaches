from rest_framework import serializers
from taches.models.commentaire_model import Commentaire

class CommentaireSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()
    reponses = serializers.SerializerMethodField()

    class Meta:
        model = Commentaire
        fields = "__all__"

    def get_reponses(self, obj):
        return CommentaireSerializer(obj.reponses.all(), many=True).data
