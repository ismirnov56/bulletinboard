from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from src.profiles.views import BBUserCreate, ActivateEmail, CreateStuffBBUser

# url-ы для работы с пользователями

urlpatterns = [
    path('users/', BBUserCreate.as_view(), name='account-create'),
    path('staff/', CreateStuffBBUser.as_view(), name='stuff-create'),
    path('users/activate/', ActivateEmail.as_view(), name='email-activate'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
