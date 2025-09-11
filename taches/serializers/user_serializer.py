# taches/serializers/user_serializer.py
from rest_framework import serializers
from taches.models.user_model import User
from drf_spectacular.utils import extend_schema_field

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_active", "groups"]

    @extend_schema_field(serializers.ListSerializer(child=serializers.CharField()))
    def get_groups(self, obj) -> list[str]:  # type hint ajouté
        return [group.name for group in obj.groups.all()]
