from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from src.profiles.views import BBUserCreate, ActivateEmail, CreateBBUserForAdmin, LoginAPIView, LogoutAPIView

# url-ы для работы с пользователями

urlpatterns = [
    path('users/', BBUserCreate.as_view(), name='account-create'),
    path('staff/', CreateBBUserForAdmin.as_view(), name='stuff-create'),
    path('users/activate/', ActivateEmail.as_view(), name='email-activate'),
    path('auth/login/', LoginAPIView.as_view(), name='token_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
