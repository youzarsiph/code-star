""" API endpoints for code_star.messages """

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from code_star.messages.models import Message
from code_star.messages.serializers import MessageSerializer
from code_star.mixins import OwnerMixin
from code_star.permissions import IsChatOwner, IsOwner


# Create your viewsets here.
class MessageViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete Messages"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsChatOwner, IsOwner)
    search_fields = ("content",)
    filterset_fields = ("chat", "role", "is_starred")
