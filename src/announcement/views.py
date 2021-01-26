from rest_framework.generics import ListAPIView, RetrieveAPIView
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


class RetrieveAnnouncement(RetrieveAPIView):
    """
    Просмотр одного объявления по uuid
    """
    queryset = Announcements.objects.filter(status='active')
    lookup_field = 'uuid'
    permission_classes = [AllowAny]
    serializer_class = AnnouncementsSerializer

    def get(self, request, *args, **kwargs):
        """
        Автоувеличение количества просмотров
        """
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save(update_fields=("views",))
        return super().get(request, *args, **kwargs)

