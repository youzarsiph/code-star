""" CodeStar URLConf """

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from code_star.chats.views import ChatViewSet
from code_star.messages.views import MessageViewSet


# Create your URLConf here.
router = DefaultRouter()
router.register("chats", ChatViewSet, "chat")
router.register("messages", MessageViewSet, "message")

urlpatterns = [
    path("", include(router.urls)),
]
