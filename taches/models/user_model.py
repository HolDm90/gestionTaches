from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models



# Utilisateur personnalisé
class User(AbstractUser):
    ROLE_CHOICES = [
        ('pending', 'En attente'),
        ('chef_equipe', 'Chef d’équipe'),
        ('membre', 'Membre d’équipe'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pending')
    is_validated = models.BooleanField(default=False)

    def is_chef_equipe(self):
        return self.role == 'chef_equipe'

    def is_membre(self):
        return self.role == 'membre'