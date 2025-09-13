# taches/serializers/user_serializer.py
from rest_framework import serializers
from taches.models.user_model import User
from drf_spectacular.utils import extend_schema_field

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "is_active",  "is_validated", "groups"]

    @extend_schema_field(serializers.ListSerializer(child=serializers.CharField()))
    def get_groups(self, obj) -> list[str]:  # type hint ajouté
        return [group.name for group in obj.groups.all()]



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_validated=False
        )
        return user
