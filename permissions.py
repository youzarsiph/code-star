""" API access permissions """

from rest_framework.permissions import BasePermission


# Create your permissions here.
class IsOwner(BasePermission):
    """Only the owner can access the resource"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsChatOwner(BasePermission):
    """Only the chat owner can access the resource"""

    def has_object_permission(self, request, view, obj):
        return obj.chat.user == request.user
