from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from src.announcement.models import Announcements
from src.announcement.serializers import AnnouncementsSerializer


class ListAnnouncements(ListAPIView):
    """
    Список всех объявлений доступный для просмотра всем
    """
    queryset = Announcements.objects.filter(status='active')
    permission_classes = [AllowAny]
    serializer_class = AnnouncementsSerializer