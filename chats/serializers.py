""" Serializers for code_star.chats """

from rest_framework import serializers
from code_star.chats.models import Chat
from code_star.users.serializers import UserSerializer


# Create your serializers here.
class ChatSerializer(serializers.ModelSerializer):
    """Serialize chats"""

    class Meta:
        """Meta data"""

        model = Chat
        read_only_fields = ("user",)
        fields = (
            "id",
            "url",
            "user",
            "title",
            "description",
            "message_count",
            "created_at",
            "updated_at",
        )


class ChatRetrieveSerializer(ChatSerializer):
    """Serializer for retrieving chat details"""

    user = UserSerializer()

    class Meta(ChatSerializer.Meta):
        """Meta data"""

        depth = 1
        fields = ChatSerializer.Meta.fields + ("messages",)
