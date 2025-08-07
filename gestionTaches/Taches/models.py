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

    def is_chef_equipe(self):
        return self.role == 'chef_equipe'

    def is_membre(self):
        return self.role == 'membre'


# Équipe
class Team(models.Model):
    nom = models.CharField(max_length=255)
    chef_equipe = models.OneToOneField("User", on_delete=models.SET_NULL, null=True, related_name="equipe_dirigee")
    members = models.ManyToManyField("User", through="TeamMembers", related_name="equipes")

    def __str__(self):
        return self.nom


# Statut de tâche
class Statut(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


# Priorité de tâche
class Priorite(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


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


# Membre d’équipe
class TeamMembers(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} dans {self.team}"


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
