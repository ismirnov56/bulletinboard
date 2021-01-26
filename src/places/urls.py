from rest_framework.routers import SimpleRouter

from src.places.views import CityView, CountryView, RegionView

urlpatterns = []

router = SimpleRouter()
router.register(r'city', CityView, basename='City')
router.register(r'country', CountryView, basename='Country')
router.register(r'region', RegionView, basename='Region')

urlpatterns += router.urls
