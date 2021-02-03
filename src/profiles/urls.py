from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from src.profiles.views import ActivateEmail, CreateModeratorUser, LoginAPIView, LogoutAPIView, CreateBBUser

# url-ы для работы с пользователями


urlpatterns = [
    path('users/', CreateBBUser.as_view(), name='account-create'),
    path('staff/', CreateModeratorUser.as_view(), name='stuff-create'),
    path('users/activate/', ActivateEmail.as_view(), name='email-activate'),
    path('login/', LoginAPIView.as_view(), name='token-login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
