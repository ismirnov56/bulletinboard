from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.profiles.urls')),
    path('api/v1/', include('src.announcement.urls')),
    path('api/v1/', include('src.places.urls'))
]
