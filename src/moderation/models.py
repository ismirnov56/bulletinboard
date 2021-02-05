from django.conf import settings
from django.db import models
from django.utils import timezone

from ..announcement.models import Announcements


class Moderation(models.Model):
    """
        Модель хранящая информацию о модерации объявлений
    """
    STATUSES = (
        ('publish', 'publish'),
        ('no_publish', 'no_publish')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name="moderator")
    announcement = models.ForeignKey(Announcements, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSES, default='no_publish')
    info_result = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'id: {self.id} moderator email: {self.user.email} announcement: {self.announcement.uuid} status: {self.status}'
