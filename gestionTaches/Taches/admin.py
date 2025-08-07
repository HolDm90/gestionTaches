from django.contrib import admin
from .models import User, Team, Statut, Priorite, Tache, TeamMembers, Commentaire

class TeamMembersInline(admin.TabularInline):  # Déclarée en premier
    model = TeamMembers
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('nom', 'chef_equipe')
    search_fields = ('nom',)
    filter_horizontal = ()  # Rien ici car ManyToMany via un modèle intermédiaire
    inlines = [TeamMembersInline] 

@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'date_ajout')
    list_filter = ('team',)
    search_fields = ('user__username',)
    

@admin.register(Statut)
class StatutAdmin(admin.ModelAdmin):
    list_display = ('label',)

@admin.register(Priorite)
class PrioriteAdmin(admin.ModelAdmin):
    list_display = ('label',)

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'equipe', 'statut', 'priorite', 'date_echeance')
    list_filter = ('statut', 'priorite', 'equipe')
    search_fields = ('titre', 'description')

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'tache', 'date_creation', 'is_deleted')
    list_filter = ('is_deleted', 'date_creation')
    search_fields = ('contenu',)
