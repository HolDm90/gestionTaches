from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models





# Membre d’équipe
class TeamMembers(models.Model):
    ROLE_CHOICES = [
        ("chef", "Chef d’équipe"),
        ("membre", "Membre d’équipe"),
    ]

    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="membre")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.role} dans {self.team}"



