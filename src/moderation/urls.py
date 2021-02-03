from django.urls import path

from src.moderation.views import CreateModeration

urlpatterns = [
    path('<announcement_uuid>', CreateModeration.as_view(), name='create-moderation'),
]
