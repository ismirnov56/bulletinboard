import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

from ..places.models import Cities


class Categories(MPTTModel):
    """
    Модель категорий испольует mptt для создания дерева категорий
    https://django-mptt.readthedocs.io/en/latest/index.html
    """
    title = models.CharField(max_length=150, blank=False),
    slug = models.SlugField(unique=True),
    description = models.TextField(blank=True),
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']


class Announcements(models.Model):
    """
    Модель объявлений
    """
    STATUSES = (
        ('draft', 'draft'),
        ('on_moderation', 'on_moderation'),
        ('rejected', 'rejected'),
        ('archive', 'archive'),
        ('active', 'active')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner")
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=13, choices=STATUSES, default='draft')

    def __str__(self):
        return f'uuid: {self.uuid} owner email: {self.user.email} status: {self.status}'


def announcements_directory_path(instance, filename):
    """
    функция для обеспечения красивой ссылки при сохранении картинки в файловую систему
    """
    return 'announcements/announcement_{0}/{1}'.format(instance.announcement.uuid, filename)


class Images(models.Model):
    """
    Модель обеспечивающая сохранение картинок, вынесена в отдельную т.к. у одного объявления может быть несколько картинок
    """
    announcement = models.ForeignKey(Announcements, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=announcements_directory_path, null=True, blank=True)

    def __str__(self):
        return f'id: {self.id} announcement: {self.announcement.uuid}'
