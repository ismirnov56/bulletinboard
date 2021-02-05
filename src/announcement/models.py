import sys
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from uuslug import uuslug
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..places.models import City


class Categories(MPTTModel):
    """
    Модель категорий испольует mptt для создания дерева категорий
    https://django-mptt.readthedocs.io/en/latest/index.html
    """
    name = models.CharField(max_length=150, blank=False)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Создание уникального slug для категории
        """
        category = self
        temp_slug = uuslug(self.name, instance=self, max_length=150)
        while category.parent:
            temp_slug = category.parent.slug + '-' + temp_slug
            category = category.parent
        self.slug = temp_slug
        super(Categories, self).save(*args, **kwargs)


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
    title = models.CharField(max_length=150, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner", blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
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
    return 'announcements/announcement{0}/{1}'.format(instance.announcement.uuid, filename)


def validate_image(image):
    """
        Валидация изображения
    """
    max_height = 300
    max_width = 300
    width, height = get_image_dimensions(image.file)
    if width <= max_width or height <= max_height:
        raise ValidationError("Height or Width is larger than what is allowed")


class Images(models.Model):
    """
    Модель обеспечивающая сохранение картинок, вынесена в отдельную т.к. у одного объявления может быть несколько картинок
    """
    announcement = models.ForeignKey(Announcements, related_name='images', on_delete=models.CASCADE, blank=False)
    image = models.ImageField(upload_to=announcements_directory_path, blank=False, validators=[validate_image])

    def __str__(self):
        return f'id: {self.id} announcement: {self.announcement.uuid}'

    def save(self, *args, **kwargs):
        """
        Изменение размера изображения при сохранении
        """
        img = Image.open(self.image)

        if img.height > 1500 or img.width > 1500:
            output_size = (img.width / 2, img.height / 2)
            img.thumbnail(output_size)
            img = img.convert('RGB')

            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            self.image = InMemoryUploadedFile(output, 'ImageField',
                                              f'{self.image.name.split(".")[0]}.jpg',
                                              'image/jpeg', sys.getsizeof(output),
                                              None)
        super().save(*args, **kwargs)