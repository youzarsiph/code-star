""" Serializers for code_star.users """

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


# Create your serializers here.
User = get_user_model()


class UserSerializer(ModelSerializer):
    """Serialize users"""

    class Meta:
        """Meta data"""

        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
