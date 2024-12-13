from django.db.models.query import F, QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from wbcore import viewsets
from wbcore.contrib.notifications.models import (
    NotificationType,
    NotificationTypeSetting,
)
from wbcore.contrib.notifications.serializers import (
    NotificationTypeRepresentationSerializer,
    NotificationTypeSettingModelSerializer,
)

from .configs.notification_types import NotificationTypeSettingDisplayConfig


class NotificationTypeRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeRepresentationSerializer


class NotificationTypeSettingModelViewSet(viewsets.ModelViewSet):
    queryset = NotificationTypeSetting.objects.all()
    serializer_class = NotificationTypeSettingModelSerializer

    display_config_class = NotificationTypeSettingDisplayConfig

    search_fields = ["notification_type__title", "notification_type__help_text"]

    def create(self, request: Request) -> Response:
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request: Request, pk=None) -> Response:
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self) -> QuerySet[NotificationTypeSetting]:
        return (
            super().get_queryset().filter(user=self.request.user).annotate(help_text=F("notification_type__help_text"))
        )
