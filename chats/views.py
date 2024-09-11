""" API endpoints for code_star.chats """

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from code_star.chats.models import Chat
from code_star.chats.serializers import ChatRetrieveSerializer, ChatSerializer
from code_star.mixins import OwnerMixin
from code_star.permissions import IsOwner


# Create your viewsets here.
class ChatViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete Chats"""

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    search_fields = ("title", "description")

    def get_serializer_class(self):
        """Return the appropriate serializer based on the action"""

        if self.action == "retrieve":
            self.serializer_class = ChatRetrieveSerializer

        return super().get_serializer_class()
