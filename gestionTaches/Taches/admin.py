from django.contrib import admin
from .models import User, Team, TeamMembers, Statut, Priorite, Tache, Commentaire

# ----------------------------
# UserAdmin
# ----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_validated', 'is_staff')
    list_filter = ('role', 'is_validated', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)


# ----------------------------
# TeamMembers Inline
# ----------------------------
class TeamMembersInline(admin.TabularInline):
    model = TeamMembers
    extra = 1


# ----------------------------
# TeamAdmin
# ----------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('nom', 'get_chef', 'count_members')
    inlines = [TeamMembersInline]

    def get_chef(self, obj):
        chef = obj.teammembers_set.filter(role='chef').first()
        return chef.user.username if chef else "-"
    get_chef.short_description = "Chef d'équipe"

    def count_members(self, obj):
        return obj.members.count()
    count_members.short_description = "Nombre de membres"


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
# TeamMembersAdmin
# ----------------------------
@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role', 'date_ajout')
    list_filter = ('role', 'team')
    search_fields = ('user__username', 'team__nom')


# ----------------------------
# CommentaireAdmin
# ----------------------------
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('tache', 'auteur', 'date_creation', 'is_deleted', 'parent')
    list_filter = ('is_deleted', 'tache')
    search_fields = ('auteur__username', 'contenu')
