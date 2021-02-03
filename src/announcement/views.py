from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from src.announcement.models import Announcements
from src.announcement.serializers import AnnouncementsListSerializer, AnnouncementsRetrieveSerializer, \
    AnnouncementsRetrieveUserSerializer
from src.base.permissions import IsAuthenticatedAndOwner


class ListActiveAnnouncements(ListAPIView):
    """
        Список всех объявлений доступный для просмотра всем
    """
    queryset = Announcements.objects.filter(status='active')
    permission_classes = [AllowAny]
    serializer_class = AnnouncementsListSerializer


class RetrieveActiveAnnouncement(RetrieveAPIView):
    """
        Просмотр одного объявления по uuid
    """
    queryset = Announcements.objects.filter(status='active')
    lookup_field = 'uuid'
    permission_classes = [AllowAny]
    serializer_class = AnnouncementsRetrieveSerializer

    def get(self, request, *args, **kwargs):
        """
        Автоувеличение количества просмотров
        Также не разрешаем пользователю набивать просмотры
        """
        obj = self.get_object()
        if obj.user != self.request.user:
            obj.views = obj.views + 1
            obj.save(update_fields=("views",))
        return super().get(request, *args, **kwargs)


class ListUserAnnouncements(ListAPIView):
    """
        Список объявлений пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementsListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['status']

    def get_queryset(self):
        return Announcements.objects.filter(user=self.request.user)


class RetrieveUserAnnouncement(RetrieveAPIView):
    """
        Объявление которое создал пользователь
    """
    queryset = Announcements.objects.filter(status='active')
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticatedAndOwner]
    serializer_class = AnnouncementsRetrieveUserSerializer


class DestroyAnnouncement(DestroyAPIView):
    """
        Удаление объявления
    """
    queryset = Announcements.objects.filter(status__in=['active', 'draft', 'rejected', 'on_moderation'])
    permission_classes = [IsAuthenticatedAndOwner]
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = 'archive'
        obj.save(update_fields=('status',))
        return Response(status=status.HTTP_204_NO_CONTENT)
