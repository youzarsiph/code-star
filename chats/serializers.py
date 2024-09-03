""" Serializers for code_star.chats """

from rest_framework import serializers


# Create your serializers here.
class ChatSerializer(serializers.Serializer):
    """Serialize code chat"""

    message = serializers.CharField(
        max_length=1000,
        required=True,
        allow_blank=False,
    )
