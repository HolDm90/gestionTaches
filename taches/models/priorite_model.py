from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models




# Priorité de tâche
class Priorite(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label