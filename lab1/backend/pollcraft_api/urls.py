from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers


@extend_schema(
    responses=inline_serializer(
        name="AboutApp",
        fields={
            "name": serializers.CharField(),
            "emblem": serializers.CharField(),
            "description": serializers.CharField(),
        },
    )
)
@api_view(["GET"])
@permission_classes([AllowAny])
def about_app(request):
    return Response(
        {
            "name": "PollCraft",
            "emblem": "PC",
            "description": (
                "PollCraft is a web application for creating polls, adding answer "
                "options, voting and viewing vote statistics."
            ),
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/about/", about_app, name="about-app"),
    path("api/auth/", include("accounts.urls")),
    path("api/collaboration/", include("collaboration.urls")),
    path("api/polls/", include("polls.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
