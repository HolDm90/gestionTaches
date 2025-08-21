from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models


# Commentaire
class Commentaire(models.Model):
    tache = models.ForeignKey("Tache", on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        prefix = "[SUPPRIMÉ] " if self.is_deleted else ""
        return f"{prefix}Commentaire de {self.auteur.username} sur {self.tache.titre}"

    def soft_delete(self):
        """Marque le commentaire comme supprimé sans le supprimer en base."""
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ['date_creation']
