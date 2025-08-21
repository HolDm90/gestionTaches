from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from .team_model import Team
from .statut_model import Statut
from .priorite_model import Priorite
from django.db import models





# Tâche
class Tache(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    equipe = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='taches')
    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, null=True)
    priorite = models.ForeignKey(Priorite, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateField(null=True, blank=True)
    date_echeance = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre