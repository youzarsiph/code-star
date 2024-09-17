""" Serializers for code_star.messages """

from rest_framework.serializers import ModelSerializer

from code_star.messages.models import Message


# Create your serializers here.
class MessageSerializer(ModelSerializer):
    """Serialize messages"""

    class Meta:
        """Meta data"""

        model = Message
        read_only_fields = ("chat", "user")
        fields = (
            "id",
            "url",
            "user",
            "role",
            "chat",
            "content",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )


class ChatMessageSerializer(MessageSerializer):
    """Serialize chat messages"""

    class Meta(MessageSerializer.Meta):
        """Meta data"""

        fields = (
            "id",
            "user",
            "role",
            "chat",
            "content",
            "is_starred",
            "is_edited",
            "created_at",
            "updated_at",
        )
