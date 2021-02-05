from rest_framework import serializers

from src.announcement.models import Announcements, Images, Categories
from src.places.serializers import CitySerializer
from src.profiles.models import BBUser


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений
    """

    class Meta:
        model = Images
        fields = ['image']


class OwnerInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для информации о владельце объявления
    """

    class Meta:
        model = BBUser
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'info']


class CategoryForAnnouncementsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для категории
    """

    class Meta:
        model = Categories
        fields = ['name']


class AnnouncementsListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка объявлений
    """
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Announcements
        fields = ['uuid', 'title', 'description', 'images', 'price', 'views', 'update_at']


class AnnouncementsUserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка объявлений пользователя
    """
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Announcements
        fields = ['uuid', 'title', 'status', 'images', 'description', 'price', 'views', 'update_at']


class AnnouncementsRetrieveSerializer(serializers.ModelSerializer):
    """
        Сериализатор для просмотра конеретного объявления
    """
    user = OwnerInfoSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    category = CategoryForAnnouncementsSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Announcements
        fields = ['uuid', 'title', 'description', 'price', 'city', 'images', 'user', 'category', 'views', 'update_at']


class AnnouncementsRetrieveUserSerializer(serializers.ModelSerializer):
    """
        Сериализатор для объявлений
    """
    images = ImageSerializer(many=True, read_only=True)
    category = CategoryForAnnouncementsSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Announcements
        fields = ['uuid', 'title', 'description', 'price', 'city', 'images', 'category', 'views', 'create_at',
                  'update_at', 'status']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    """
        Сериализатор для создания объявлений
    """

    class Meta:
        model = Announcements
        fields = ['uuid', 'title', 'description', 'price', 'city', 'category', 'views', 'status']