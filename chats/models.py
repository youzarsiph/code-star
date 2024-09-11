""" Data models for code_star.chats """

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
User = get_user_model()


class Chat(models.Model):
    """CodeStar Chats"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Chat owner",
    )
    title = models.CharField(
        max_length=64,
        db_index=True,
        default="Untitled chat",
        help_text="Chat title",
    )
    description = models.CharField(
        max_length=512,
        db_index=True,
        default="Untitled chat",
        help_text="Chat description",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update",
    )

    def __str__(self) -> str:
        return self.title

    @property
    def message_count(self) -> int:
        """Number of messages in the chat"""

        return self.messages.count()
