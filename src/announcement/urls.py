from django.urls import path

# url-ы для работы с объявлениями
from src.announcement.views import ListActiveAnnouncements, RetrieveActiveAnnouncement, DestroyAnnouncement,\
    ListUserAnnouncements, RetrieveUserAnnouncement

urlpatterns = [
    path('', ListActiveAnnouncements.as_view(), name='announcements-list'),
    path('<uuid>', RetrieveActiveAnnouncement.as_view(), name='announcements-detail'),
    path('me/', ListUserAnnouncements.as_view(), name='user-announcements-list'),
    path('me/<uuid>', DestroyAnnouncement.as_view(), name='announcements-delete'),
    path('me/<uuid>', RetrieveUserAnnouncement.as_view(), name='user-announcements-delete')
]
