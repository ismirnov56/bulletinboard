from rest_framework import serializers

from src.places.models import Country, Region, City


class CountrySerializer(serializers.ModelSerializer):
    """
    Сериализатор для стран
    """

    class Meta:
        model = Country
        fields = ['name', 'slug']


class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регионов
    """
    country = CountrySerializer()

    class Meta:
        model = Region
        fields = ['name', 'slug', 'country']


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для городов
    """
    region = RegionSerializer()

    class Meta:
        model = City
        fields = ['name', 'slug', 'region']


class CityPlaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для городов CRUD Admin and users read only
    """

    class Meta:
        model = City
        fields = ['name', 'slug', 'region']


class RegionPlaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регионов CRUD Admin and users read only
    """

    class Meta:
        model = Region
        fields = ['name', 'slug', 'country']

