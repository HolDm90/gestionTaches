""" from taches.serializers.user_serializer import UserSerializer
from taches.serializers.team_serializer import TeamSerializer
from taches.serializers.team_member_serializer import TeamMemberSerializer
from taches.serializers.statut_serializer import StatutSerializer
from taches.serializers.priorite_serializer import PrioriteSerializer
from taches.serializers.tache_serializer import TacheSerializer
from taches.serializers.commentaire_serializer import CommentaireSerializer """

from .user_serializer import UserSerializer
from .team_serializer import TeamSerializer
from .statut_serializer import StatutSerializer
from .priorite_serializer import PrioriteSerializer
from .tache_serializer import TacheSerializer
from .team_member_serializer import TeamMembersSerializer
from .commentaire_serializer import CommentaireSerializer


__all__ = [
    "UserSerializer",
    "TeamSerializer",
    "TeamMembersSerializer",
    "StatutSerializer",
    "PrioriteSerializer",
    "TacheSerializer",
    "CommentaireSerializer",
]
