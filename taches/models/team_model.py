from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models



# Équipe
class Team(models.Model):
    nom = models.CharField(max_length=255)
    members = models.ManyToManyField("User", through="TeamMembers", related_name="equipes")

    def __str__(self):
        return self.nom
