""" CodeCompletion consumers """

from typing import Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from huggingface_hub import InferenceClient

from code_star.completions.serializers import CompletionSerializer
from code_star.mixins import SerializerValidationMixin


# Create your consumers here.
class CompletionConsumer(SerializerValidationMixin, AsyncJsonWebsocketConsumer):
    """Code completion consumer"""

    client = InferenceClient()
    serializer_class = CompletionSerializer

    async def receive_json(self, content: Dict[str, str] | None, **kwargs) -> None:
        """Receive JSON data from the websocket"""

        # If data validation fails, stop execution
        if content is None:
            return

        # This can be used as loading indicator
        await self.send_json({"generating": True})

        try:
            # Code completion
            completion = self.client.text_generation(
                prompt=content["prompt"],
                model="bigcode/starcoder2-15b",
                max_new_tokens=512,
            )

            await self.send_json({"generating": False, "response": completion})

        except Exception as error:
            # Send error message
            await self.send_json({"generating": False, "error": str(error)})

            # Close the connection
            await self.close()
