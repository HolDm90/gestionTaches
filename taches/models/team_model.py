from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from .commentaire_model import Commentaire


class Team(models.Model):
    nom = models.CharField(max_length=255)
    members = models.ManyToManyField("User", through="TeamMembers", related_name="equipes")

    # ✅ Ajout de la relation générique
    commentaires = GenericRelation(Commentaire)

    def __str__(self):
        return self.nom
