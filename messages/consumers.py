""" Consumers for code_star.messages """

from typing import Any, Dict
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from code_star.messages.models import Message
from code_star.messages.serializers import MessageSerializer
from code_star.consumers import SerializerValidationMixin


# Create your consumers here.
class AsyncMessageConsumer(SerializerValidationMixin, AsyncJsonWebsocketConsumer):
    """Message AsyncJsonWebsocketConsumer"""

    model = Message
    serializer_class = MessageSerializer

    @database_sync_to_async
    def get_instance(self, pk: int):
        """Get an instance of self.model"""

        return self.model.objects.get(pk=pk)

    @database_sync_to_async
    def perform_create(self, serializer) -> None:
        """Create an instance"""

        serializer.save()

    async def model_create(self, event: Dict["str", Any]) -> None:
        """Create an instance of self.model"""

        serializer = self.get_serializer(data=event["data"])
        await self.perform_create(serializer)
        await self.send_json({"type": "model.create", "data": serializer.data})

    async def model_list(self, event: Dict["str", Any]) -> None:
        pass

    async def model_delete(self, event: Dict["str", Any]) -> None:
        pass

    async def model_update(self, event: Dict["str", Any]) -> None:
        """update an instance of self.model"""

        instance = await self.get_instance(event["data"]["id"])
        serializer = self.get_serializer(instance=instance, data=event["data"])
        serializer.is_valid(raise_exception=True)
        await self.perform_create(serializer)
        await self.send_json({"type": "model.create", "data": serializer.data})
