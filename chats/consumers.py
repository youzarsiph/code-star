""" Chat consumers """

from typing import Any, Dict, List, Literal
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from huggingface_hub import AsyncInferenceClient

from code_star.chats.models import Chat
from code_star.consumers import SerializerValidationMixin
from code_star.messages.models import Message
from code_star.messages.serializers import ChatMessageSerializer


# Create your consumers here.
class ChatConsumer(SerializerValidationMixin, AsyncJsonWebsocketConsumer):
    """Chat consumer"""

    client = AsyncInferenceClient("HuggingFaceH4/starchat2-15b-v0.1")
    serializer_class = ChatMessageSerializer
    messages = [
        {
            "role": "system",
            "content": "You are CodeStar, an advanced AI-powered coding assistant designed to enhance "
            "developer productivity by providing intelligent code suggestions and natural "
            "language interactions.",
        }
    ]

    async def connect(self) -> None:
        """Init self.chat"""

        # User
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close(code=401, reason="Authentication")
            return

        # Chat
        self.chat = await self.get_chat(id=self.scope["url_route"]["kwargs"]["pk"])

        # Check if the user is authorized to view the chat
        if self.chat is None or self.user.id != self.chat.user_id:
            await self.close(code=403, reason="Authorization")
            return

        # Chat history
        self.messages.extend(await self.get_messages())

        return await super().connect()

    async def receive_json(self, content: Dict[str, str] | None, **kwargs) -> None:
        """Receive JSON data from the websocket"""

        # If data validation fails, stop execution
        if content is None:
            return

        # User's message
        message = await self.create_message(
            role=True,
            as_dict=True,
            content=content["content"],
        )

        # Send the message
        await self.send_json({"generating": True, "data": message})

        try:
            response = await self.client.chat_completion(
                messages=self.messages,
                max_tokens=1024,
            )

            # LLM message
            llm_message = await self.create_message(
                role=False,
                as_dict=True,
                content=str(response.choices[0].message.content),
            )

            # Send the message
            await self.send_json({"generating": False, "data": llm_message})

        except Exception as error:
            # Send error message
            await self.send_json({"generating": False, "error": str(error)})

            # Close the connection
            await self.close()

    @database_sync_to_async
    def create_message(
        self,
        role: bool,
        content: str,
        as_dict: bool = False,
    ) -> Message | Dict[str, Any]:
        """Create a message"""

        message = self.chat.messages.create(
            user=self.user,
            role=role,
            content=content,
        )

        # Add User's message to chat history
        self.messages.append(
            {
                "role": "user" if message.role else "assistant",
                "content": message.content,
            }
        )

        if as_dict:
            return self.get_serializer(
                instance=message,
                context={"request": self.scope},
            ).data

        return message

    @database_sync_to_async
    def get_chat(self, id: int) -> Chat | None:
        """Return chat instance"""

        try:
            return Chat.objects.filter(user=self.user).get(pk=id)

        except Chat.DoesNotExist:
            return

    @database_sync_to_async
    def get_messages(self) -> List[Dict[Literal["role", "content"], str]]:
        """Get chat history"""

        return [
            {
                "role": (
                    "user"
                    if message.role
                    else "assistant" if not message.role else "system"
                ),
                "content": message.content,
            }
            for message in self.chat.messages.all()
        ]
