from rest_framework import serializers
from taches.models.tache_model import Tache
from taches.models.team_model import Team
from taches.models.statut_model import Statut
from taches.models.priorite_model import Priorite

class TacheSerializer(serializers.ModelSerializer):
    equipe = serializers.StringRelatedField(read_only=True)
    priorite = serializers.SlugRelatedField(
        queryset=Priorite.objects.all(),
        slug_field='label',
        required=False
    )
    statut = serializers.StringRelatedField(read_only=True)

    # Champs write-only pour sécuriser les mises à jour
    statut_id = serializers.PrimaryKeyRelatedField(
        queryset=Statut.objects.all(),
        write_only=True,
        required=False,
        source='statut'
    )

    equipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        write_only=True,
        required=False,
        source='equipe'
    )

    class Meta:
        model = Tache
        fields = [
            'id', 'titre', 'description',
            'equipe', 'equipe_id',
            'statut', 'statut_id',
            'priorite',
            'date_debut', 'date_echeance', 'date_creation', 'date_mise_a_jour'
        ]
