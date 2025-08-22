# taches/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views.user_view import RegisterView, LogoutView, CustomTokenObtainPairView
from .views import (
    UserViewSet, TeamViewSet, StatutViewSet,
    PrioriteViewSet, TacheViewSet, TeamMembersViewSet,
    CommentaireViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'statuts', StatutViewSet)
router.register(r'priorites', PrioriteViewSet)
router.register(r'taches', TacheViewSet)
router.register(r'team-members', TeamMembersViewSet)
router.register(r'commentaires', CommentaireViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
