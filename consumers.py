""" Base consumers """

import json
from typing import Dict
from rest_framework.serializers import Serializer


# Create your consumers here.
class SerializerValidationMixin:
    """Validates incoming data using a Serializer"""

    serializer_class = None

    def get_serializer_class(self) -> Serializer:
        """Return self.serializer_class if not None"""

        if self.serializer_class is None:
            raise Exception("self.serializer_class can not be None.")

        if isinstance(self.serializer_class, Serializer):
            raise Exception("self.serializer_class is not an instance of Serializer.")

        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """Instantiate and return self.serializer_class"""

        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    async def decode_json(self, text_data) -> Dict[str, str] | None:
        """Decode and validate incoming data"""

        # Convert to python
        data = json.loads(text_data)

        # Data validation
        serializer = self.get_serializer(data=data["data"])

        if serializer.is_valid():
            return serializer.validated_data

        # Send error messages
        await self.send_json(serializer.errors)
