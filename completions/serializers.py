""" Serializers for code_star.completions """

from rest_framework import serializers


# Create your serializers here.
class CompletionSerializer(serializers.Serializer):
    """Serialize code completions"""

    prompt = serializers.CharField(
        max_length=1000,
        required=True,
        allow_blank=False,
    )
