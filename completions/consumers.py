""" CodeCompletion consumers """

from typing import Any, Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from huggingface_hub import AsyncInferenceClient

from code_star.completions.serializers import CompletionSerializer
from code_star.consumers import SerializerValidationMixin


# Create your consumers here.
class CompletionConsumer(SerializerValidationMixin, AsyncJsonWebsocketConsumer):
    """Code completion consumer"""

    client = AsyncInferenceClient()
    serializer_class = CompletionSerializer

    async def connect(self) -> None:
        """Perform checks before accepting connection"""

        # User
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close(code=401, reason="Authentication")
            return

        return await super().connect()

    async def receive_json(self, content: Dict[str, Any] | None, **kwargs) -> None:
        """Receive JSON data from the websocket"""

        # If data validation fails, stop execution
        if content is None:
            return

        # This can be used as loading indicator
        await self.send_json({"generating": True})

        prompt = content["prompt"]

        try:
            # Code completion
            completion = await self.client.text_generation(
                prompt=prompt,
                model="bigcode/starcoder2-15b",
                max_new_tokens=512,
            )

            await self.send_json(
                {
                    "generating": False,
                    "response": prompt + completion,
                }
            )

        except Exception as error:
            # Send error message
            await self.send_json({"generating": False, "error": str(error)})

            # Close the connection
            await self.close()
