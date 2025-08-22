from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from taches.models.user_model import User
from taches.models.team_model import Team
from taches.models.team_member_model import TeamMembers
from taches.models.tache_model import Tache
from taches.models.commentaire_model import Commentaire


class Command(BaseCommand):
    help = "Créer des utilisateurs, équipes, tâches et commentaires de test"

    def add_arguments(self, parser):
        parser.add_argument("n_users", type=int, help="Nombre d'utilisateurs à créer")
        parser.add_argument("n_teams", type=int, help="Nombre d'équipes à créer")

    def handle(self, *args, **kwargs):
        n_users = kwargs["n_users"]
        n_teams = kwargs["n_teams"]

        users = []
        task_status = ["en_attente", "en_cours", "terminee"]
        task_priorites = ["basse", "moyenne", "haute"]

        # 🔹 Création des utilisateurs
        for i in range(1, n_users + 1):
            username = f"user{i}"
            email = f"user{i}@test.com"
            role = random.choice(["chef_equipe", "membre"])

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    role=role,
                    is_validated=True,
                    password="TestPassword123"
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f"✅ Utilisateur: {username} ({role})"))
            else:
                users.append(User.objects.get(username=username))
                self.stdout.write(self.style.WARNING(f"⚠️ {username} existe déjà"))

        # 🔹 Création des équipes + tâches
        for t in range(1, n_teams + 1):
            team, created = Team.objects.get_or_create(nom=f"Equipe{t}")
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Équipe: {team.nom}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ {team.nom} existe déjà"))

            # Membres de l'équipe
            team_users = random.sample(users, min(len(users), random.randint(3, 6)))

            # Chef
            chef = random.choice(team_users)
            TeamMembers.objects.get_or_create(team=team, user=chef, role="chef")

            # Membres
            for u in team_users:
                if u != chef:
                    TeamMembers.objects.get_or_create(team=team, user=u, role="membre")

            self.stdout.write(
                self.style.SUCCESS(f"👥 {team.nom} -> Chef: {chef.username}, Membres: {[u.username for u in team_users]}")
            )

            # 🔹 Création de quelques tâches
            for j in range(1, random.randint(2, 5)):  # 2 à 4 tâches par équipe
                statut = random.choice(task_status)
                priorite = random.choice(task_priorites)
                deadline = timezone.now() + timedelta(days=random.randint(1, 30))  # deadline entre 1 et 30 jours

                tache = Tache.objects.create(
                    titre=f"Tâche {j} de {team.nom}",
                    description=f"Ceci est une tâche auto-générée pour {team.nom}",
                    equipe=team,
                    createur=chef,
                    statut=statut,
                    priorite=priorite,
                    date_echeance=deadline,
                    date_creation=timezone.now()
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"📝 Tâche: {tache.titre} (Statut: {statut}, Priorité: {priorite}, Deadline: {deadline.date()})"
                    )
                )

                # 🔹 Ajout de commentaires sur la tâche
                for k in range(random.randint(1, 3)):  # 1 à 3 commentaires
                    auteur = random.choice(team_users)
                    commentaire = Commentaire.objects.create(
                        tache=tache,
                        auteur=auteur,
                        contenu=f"Commentaire {k+1} sur {tache.titre} par {auteur.username}",
                        date_creation=timezone.now()
                    )
                    self.stdout.write(f"💬 Commentaire de {auteur.username}")

                    # 🔹 Ajout de réponses (50% des cas)
                    if random.random() > 0.5:
                        reponse_auteur = random.choice(team_users)
                        reponse = Commentaire.objects.create(
                            tache=tache,
                            auteur=reponse_auteur,
                            contenu=f"Réponse à {auteur.username} par {reponse_auteur.username}",
                            parent=commentaire,
                            date_creation=timezone.now()
                        )
                        self.stdout.write(f"↪️ Réponse de {reponse_auteur.username} à {auteur.username}")
