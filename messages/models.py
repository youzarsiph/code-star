""" Data Models for code_star.messages """

from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class Message(models.Model):
    """CodeStar messages"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        help_text="Message owner",
    )
    chat = models.ForeignKey(
        "chats.Chat",
        on_delete=models.CASCADE,
        related_name="messages",
        help_text="Message chat",
    )
    role = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        help_text="Message role, 'user' if role is True 'assistant' if False else 'system'",
    )
    content = models.TextField(
        db_index=True,
        help_text="Message content",
    )
    is_starred = models.BooleanField(
        default=False,
        help_text="Designates if the message is saved",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update",
    )

    @property
    def is_edited(self) -> bool:
        """Designates if the message is edited"""

        return self.created_at != self.updated_at

    def __str__(self) -> str:
        return f"{'user' if self.role else 'assistant' if not self.role else 'system'}: {self.content[:10]}..."
