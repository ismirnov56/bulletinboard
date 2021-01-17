from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status, generics, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from src.base.permissions import IsAdminUser
from src.profiles.models import BBUser
from src.profiles.serializers import CreateBBUserSerializer, CreateStaffBBUserSerializer
from src.profiles.tasks import send_email_task


class BBUserCreate(generics.GenericAPIView):
    """
    View для создания пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = CreateBBUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = BBUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        activate_link = reverse('email-activate')
        activate_url = 'http://' + current_site + activate_link + "?token=" + str(token)
        email_body = 'Доброго времени суток ' + user.email + \
                     '\n Используйте данную ссылку для активации вашего аккаунта \n' \
                     + activate_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        send_email_task.delay(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class ActivateEmail(views.APIView):
    """
    View для активации аккаунта
    """

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = BBUser.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            else:
                return Response({'error': 'Invalid activation url'})
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class CreateStuffBBUser(generics.GenericAPIView):
    """
    View для создания пользователя с правми модератор
    """
    permission_classes = [IsAdminUser]
    serializer_class = CreateStaffBBUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
