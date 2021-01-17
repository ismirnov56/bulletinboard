from django.urls import path

# url-ы для работы с объявлениями
from src.announcement.views import ListAnnouncements

urlpatterns = [
    path('announcements/', ListAnnouncements.as_view(), name='announcements-list'),
]
