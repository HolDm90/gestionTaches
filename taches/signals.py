from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.conf import settings
from taches.models.user_model import User


@receiver(post_save, sender=User)
def send_validation_email(sender, instance, created, **kwargs):
    """
    Quand un utilisateur est validé (is_validated=True),
    on lui envoie un email de confirmation.
    """
    if not created and instance.is_validated:
        # Vérifie qu'il n'est plus dans "Pending"
        if not instance.groups.filter(name="Pending").exists():
            subject = "Votre compte a été validé !"
            message = (
                f"Bonjour {instance.first_name or instance.email},\n\n"
                f"Votre compte a été validé par l'administrateur.\n"
                f"Vous pouvez maintenant vous connecter avec votre email : {instance.email}\n\n"
                f"Cordialement,\nL'équipe."
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False
            )


@receiver(post_save, sender=User)
def assign_pending_group(sender, instance, created, **kwargs):
    """
    Lorsqu'un nouvel utilisateur est créé,
    on l'ajoute automatiquement dans le groupe "Pending".
    """
    if created and not instance.is_superuser:
        pending_group, _ = Group.objects.get_or_create(name="Pending")
        instance.groups.add(pending_group)


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    # Création automatique des groupes par défaut après migration
    """
    if sender.name == "auth":  # éviter de le lancer pour toutes les apps
        default_groups = ["Pending", "Chef d’équipe", "Membre d’équipe"]
        for group_name in default_groups:
            Group.objects.get_or_create(name=group_name)
