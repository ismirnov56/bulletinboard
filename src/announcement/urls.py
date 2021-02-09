from django.urls import path

# url-ы для работы с объявлениями
from rest_framework.routers import SimpleRouter

from src.announcement.views import ListActiveAnnouncements, RetrieveActiveAnnouncement, DestroyAnnouncement,\
    ListUserAnnouncements, RetrieveUserAnnouncement, CreateAnnouncement, CreateImagesForAnnouncement, \
    UpdateImage, UpdateAnnouncement, DestroyImage

urlpatterns = [
    path('', ListActiveAnnouncements.as_view(), name='announcements-list'),
    path('<uuid>', RetrieveActiveAnnouncement.as_view(), name='announcements-detail'),
    path('me/', ListUserAnnouncements.as_view(), name='announcements-list-for-owner'),
    path('me/<uuid>', DestroyAnnouncement.as_view(), name='announcement-delete-for-owner'),
    path('me/<uuid>', RetrieveUserAnnouncement.as_view(), name='user-announcements-detail'),
    path('me/create/', CreateAnnouncement.as_view(), name='user-announcements-create'),
    path('me/update/<uuid>', UpdateAnnouncement.as_view(), name='user-announcements-update'),
    path('me/image/<announcement_uuid>', CreateImagesForAnnouncement.as_view(),
         name='image-create-for-announcements'),
    path('me/image/update/<pk>', UpdateImage.as_view(),
         name='update-image'),
    path('me/image/<pk>', DestroyImage.as_view(),
         name='destroy-image')
]
