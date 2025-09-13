from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail
from django.contrib.auth.models import Group


from .models import User, Team, TeamMembers, Statut, Priorite, Tache, Commentaire

# ----------------------
# UserAdmin
# ----------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'first_name', 'last_name',
        'is_validated', 'get_groups', 'is_staff', 'is_superuser'
    )
    list_filter = ('is_validated', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': (
                'is_validated', 'is_staff', 'is_active',
                'is_superuser', 'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_validated', 'groups')}
        ),
    )

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groups'

    # ✅ Actions personnalisées
    actions = ['validate_as_chef', 'validate_as_membre']

    def validate_as_chef(self, request, queryset):
        chef_group, _ = Group.objects.get_or_create(name="Chef d’équipe")
        pending_group, _ = Group.objects.get_or_create(name="Pending")

        for user in queryset:
            if not user.is_superuser:
                user.is_validated = True
                user.save()
                user.groups.remove(pending_group)
                user.groups.add(chef_group)

                # Envoi d’email
                subject = "Votre compte a été validé comme Chef d’équipe"
                message = (
                    f"Bonjour {user.first_name},\n\n"
                    f"Votre compte a été validé et vous êtes désormais Chef d’équipe.\n"
                    f"Vous pouvez vous connecter avec votre email : {user.email}\n"
                )
                send_mail(subject, message, None, [user.email], fail_silently=False)

        self.message_user(request, "Les utilisateurs sélectionnés ont été validés comme Chef d’équipe.")

    validate_as_chef.short_description = "Valider comme Chef d’équipe"

    def validate_as_membre(self, request, queryset):
        membre_group, _ = Group.objects.get_or_create(name="Membre d’équipe")
        pending_group, _ = Group.objects.get_or_create(name="Pending")

        for user in queryset:
            if not user.is_superuser:
                user.is_validated = True
                user.save()
                user.groups.remove(pending_group)
                user.groups.add(membre_group)

                # Envoi d’email
                subject = "Votre compte a été validé comme Membre d’équipe"
                message = (
                    f"Bonjour {user.first_name},\n\n"
                    f"Votre compte a été validé et vous êtes désormais Membre d’équipe.\n"
                    f"Vous pouvez vous connecter avec votre email : {user.email}\n"
                )
                send_mail(subject, message, None, [user.email], fail_silently=False)

        self.message_user(request, "Les utilisateurs sélectionnés ont été validés comme Membre d’équipe.")

    validate_as_membre.short_description = "Valider comme Membre d’équipe"

# ----------------------
# TeamMembersAdmin
# ----------------------
@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ('team', 'user', 'get_groups', 'date_joined')
    list_filter = ('team', 'user__groups')
    search_fields = ('user__email', 'team__nom')

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.user.groups.all()])
    get_groups.short_description = 'Groups'


# ----------------------
# TeamAdmin
# ----------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('nom', 'get_members', 'commentaires_count')
    search_fields = ('nom',)

    def get_members(self, obj):
        return ", ".join([member.user.email for member in obj.teammembers.all()])
    get_members.short_description = 'Membres'

    def commentaires_count(self, obj):
        return obj.commentaires.count()
    commentaires_count.short_description = 'Nombre de commentaires'


# ----------------------------
# StatutAdmin
# ----------------------------
@admin.register(Statut)
class StatutAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


# ----------------------------
# PrioriteAdmin
# ----------------------------
@admin.register(Priorite)
class PrioriteAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


# ----------------------------
# TacheAdmin
# ----------------------------
@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'equipe', 'statut', 'priorite', 'date_debut', 'date_echeance', 'date_creation')
    list_filter = ('statut', 'priorite', 'equipe')
    search_fields = ('titre', 'description')


# ----------------------------
# CommentaireAdmin
# ----------------------------
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cible', 'auteur', 'get_parent', 'date_creation', 'is_deleted', 'get_reponses_count')
    list_filter = ('content_type', 'is_deleted', 'date_creation')
    search_fields = ('contenu', 'auteur__email')

    def get_cible(self, obj):
        """
        Affiche l’objet cible via ContentType (Team, Tache, etc.)
        """
        if obj.content_type and obj.object_id:
            model_class = obj.content_type.model_class()
            try:
                instance = model_class.objects.get(id=obj.object_id)
                if hasattr(instance, 'titre'):
                    return f"{obj.content_type.model} : {instance.titre}"
                elif hasattr(instance, 'nom'):
                    return f"{obj.content_type.model} : {instance.nom}"
                else:
                    return f"{obj.content_type.model} #{obj.object_id}"
            except model_class.DoesNotExist:
                return f"{obj.content_type.model} #{obj.object_id} (supprimé)"
        return None
    get_cible.short_description = 'Cible'

    def get_parent(self, obj):
        return obj.parent.id if obj.parent else None
    get_parent.short_description = 'Parent'

    def get_reponses_count(self, obj):
        return obj.reponses.count()
    get_reponses_count.short_description = 'Nb réponses'
