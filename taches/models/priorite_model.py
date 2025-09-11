from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from .commentaire_model import Commentaire


class Priorite(models.Model):
    label = models.CharField(max_length=50)
    commentaires = GenericRelation(Commentaire)  # ✅ optionnel

    def __str__(self):
        return self.label
