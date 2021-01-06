from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from src.profiles.models import BBUser
from src.profiles.serializers import CreateBBUserSerializer
from src.profiles.tasks import send_email


class BBUserCreate(generics.GenericAPIView):
    """
    View для создания пользователя
    """
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
        email_body = 'Hi ' + user.email + \
                     ' Use the link below to verify your email \n' + activate_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        send_email.delay(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class ActivateEmail(views.APIView):
    pass
