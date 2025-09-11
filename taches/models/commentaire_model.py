from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Commentaire(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    # ✅ Relation générique
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    cible = GenericForeignKey("content_type", "object_id")

    # ✅ Réponses imbriquées
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="reponses"
    )

    def __str__(self):
        prefix = "[SUPPRIMÉ] " if self.is_deleted else ""
        return f"{prefix}Commentaire de {self.auteur.username} sur {self.cible}"

    def soft_delete(self):
        """Marque le commentaire comme supprimé sans suppression physique."""
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ["date_creation"]
