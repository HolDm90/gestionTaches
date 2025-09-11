# taches/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from taches.views.change_password_view import ChangePasswordView

from taches.views.user_view import RegisterView, LogoutView, CustomTokenObtainPairView, UserViewSet, MeView

from taches.views.team_view import TeamViewSet
from taches.views.team_member_view import TeamMembersViewSet
from taches.views.tache_view import TacheViewSet
from taches.views.statut_view import StatutViewSet
from taches.views.priorite_view import PrioriteViewSet
from taches.views.commentaire_view import CommentaireViewSet



# Router DRF pour les viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'team-members', TeamMembersViewSet)
router.register(r'taches', TacheViewSet)
router.register(r'statuts', StatutViewSet)
router.register(r'priorites', PrioriteViewSet)
router.register(r'commentaires', CommentaireViewSet)

# URL patterns
urlpatterns = [
    # Auth / JWT
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("me/", MeView.as_view(), name="me"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Toutes les routes des viewsets
    path('', include(router.urls)),
]
