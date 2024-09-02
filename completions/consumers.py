""" Code completion consumers """

import json
from typing import Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from huggingface_hub import InferenceClient
from code_star.completions.serializers import CompletionSerializer


# Create your consumers here.
class CompletionConsumer(AsyncJsonWebsocketConsumer):
    """Code completion consumer"""

    client = InferenceClient()

    async def receive_json(self, content: Dict[str, str], **kwargs) -> None:
        """Receive JSON data from the websocket"""

        # Prompt
        prompt = content["prompt"]

        response = self.client.text_generation(
            prompt=prompt,
            model="bigcode/starcoder2-15b",
            max_new_tokens=512,
        )

        await self.send_json({"response": prompt + response})

    async def decode_json(self, text_data) -> Dict[str, str]:
        """Decode and validate incoming data"""

        # Convert to python
        data = json.loads(text_data)

        # Data validation
        serializer = CompletionSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data
