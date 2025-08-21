# taches/serializers/priorite_serializer.py
from rest_framework import serializers
from taches.models.priorite_model import Priorite

class PrioriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priorite
        fields = "__all__"
