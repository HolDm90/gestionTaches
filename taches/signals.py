from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.core.mail import send_mail
from taches.models.user_model import User
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(post_save, sender=User)
def send_validation_email(sender, instance, created, **kwargs):
    # On envoie un email seulement si l'utilisateur vient d'être validé
    if not created and instance.is_validated and instance.role != 'pending':
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


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "auth":  # éviter que ça tourne pour toutes les apps
        default_groups = ["Pending", "Chef d’équipe", "Membre d’équipe"]
        for group_name in default_groups:
            Group.objects.get_or_create(name=group_name)