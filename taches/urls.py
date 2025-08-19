from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    TeamViewSet,
    StatutViewSet,
    PrioriteViewSet,
    TacheViewSet,
    TeamMembersViewSet,
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

urlpatterns = router.urls
