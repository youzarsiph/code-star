""" Chat consumers """

from typing import Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from huggingface_hub import InferenceClient

from code_star.chats.serializers import ChatSerializer
from code_star.mixins import SerializerValidationMixin


# Create your consumers here.
class ChatConsumer(SerializerValidationMixin, AsyncJsonWebsocketConsumer):
    """Chat consumer"""

    client = InferenceClient()
    serializer_class = ChatSerializer
    messages = [
        {
            "role": "system",
            "content": """
            You are CodeStar, an advanced AI-powered coding assistant designed to enhance
            developer productivity by providing intelligent code suggestions and natural
            language interactions.
            """,
        }
    ]

    async def receive_json(self, content: Dict[str, str] | None, **kwargs) -> None:
        """Receive JSON data from the websocket"""

        # If data validation fails, stop execution
        if content is None:
            return

        # User's message
        message = content["message"]

        # Add User's message to chat history
        self.messages.append({"role": "user", "content": message})

        # Send the message back
        await self.send_json({"user": message})

        # This can be used as loading indicator
        await self.send_json({"generating": True})

        try:
            response = self.client.chat_completion(
                messages=self.messages,
                model="HuggingFaceH4/starchat2-15b-v0.1",
                max_tokens=1024,
            )

            # LLM message
            llm_message = response.choices[0].message.content

            # Add LLM message to chat history
            self.messages.append({"role": "assistant", "content": str(llm_message)})

            # Send the message
            await self.send_json({"generating": False, "response": llm_message})

        except Exception as error:
            # Send error message
            await self.send_json({"generating": False, "error": str(error)})

            # Close the connection
            await self.close()
