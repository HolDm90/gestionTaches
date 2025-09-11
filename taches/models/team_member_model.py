from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.conf import settings

class TeamMembers(models.Model):
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        related_name="teammembers"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teammembers"
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team", "user")  # ✅ un user ne peut pas être ajouté 2x à la même équipe

    def __str__(self):
        return f"{self.user.email} → {self.team.nom}"
