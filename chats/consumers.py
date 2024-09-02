""" Code completion consumers """

import json
from typing import Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from huggingface_hub import InferenceClient
from code_star.chats.serializers import ChatSerializer


# Create your consumers here.
class ChatConsumer(AsyncJsonWebsocketConsumer):
    """Chat consumer"""

    client = InferenceClient()
    messages = [
        {
            "role": "system",
            "content": """You are CodeStar, an advanced AI-powered coding assistant designed to enhance developer productivity by providing intelligent code suggestions and natural language interactions.""",
        }
    ]

    async def receive_json(self, content: Dict[str, str], **kwargs) -> None:
        """Receive JSON data from the websocket"""

        # User's message
        message = content["message"]

        # Add User's message to chat history
        self.messages.append({"role": "user", "content": message})

        # Send the message back
        await self.send_json({"user": message})

        response = self.client.chat_completion(
            messages=self.messages,
            model="HuggingFaceH4/starchat2-15b-v0.1",
            max_tokens=1024,
        )

        # LLM message
        llm_message = response.choices[0].message.content

        # Add LLM message to chat history
        self.messages.append({"role": "assistant", "content": llm_message})

        # Send the message
        await self.send_json({"response": llm_message})

    async def decode_json(self, text_data) -> Dict[str, str]:
        """Decode and validate incoming data"""

        # Convert to python
        data = json.loads(text_data)

        # Data validation
        serializer = ChatSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data
