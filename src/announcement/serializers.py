from rest_framework import serializers

from src.announcement.models import Announcements, Images


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений
    """
    class Meta:
        model = Images
        fields = ['image']


class AnnouncementsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объявлений
    """
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Announcements
        fields = ['uuid', 'title', 'description', 'price', 'images', 'views', 'create_at', 'update_at', 'status']