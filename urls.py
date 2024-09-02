""" URL Configuration for code_star """

from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create your URLConf here.
router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]
