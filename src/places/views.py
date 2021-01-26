from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from src.base.permissions import IsAdminOrReadOnly
from src.places.serializers import CountrySerializer, CityPlaceSerializer, RegionPlaceSerializer
from src.places.models import City, Country, Region


class CityView(ModelViewSet):
    """
    View для городов
    CRUD для администратора
    Read-only для всех
    """
    queryset = City.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CityPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['region']


class RegionView(ModelViewSet):
    """
    View для регионов
    CRUD для администратора
    Read-only для всех
    """
    queryset = Region.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = RegionPlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['country']


class CountryView(ModelViewSet):
    """
    View для стран
    CRUD для администратора
    Read-only для всех
    """
    queryset = Country.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CountrySerializer
