from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class AccountsTestVerify(APITestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(email='noverify@example.com', phone='+9(999)9999999',
                                                              password='testpassword159789')
        self.test_user_verify = get_user_model().objects.create_stuff_user(email='verify@example.com', phone='+8(999)9999999',
                                                                     password='testpassword159789')
        self.test_user_blocked = get_user_model().objects.create_stuff_user(email='blocked@example.com',
                                                                           phone='+1(999)9999999',
                                                                           password='testpassword159789')
        self.test_user_blocked.is_verify = True
        self.test_user_blocked.save()
        self.test_user_verify.is_verify = True
        self.test_user_verify.is_active = True
        self.test_user_verify.save()

    def test_verify(self):
        token = RefreshToken.for_user(self.test_user).access_token
        activate_link = reverse('email-activate')
        activate_url = activate_link + "?token=" + str(token)
        response = self.client.get(activate_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.is_active)
        self.assertTrue(self.test_user.is_verify)

    def test_bad_verify(self):
        token = RefreshToken.for_user(self.test_user_verify).access_token
        activate_link = reverse('email-activate')
        activate_url = activate_link + "?token=" + str(token)
        response = self.client.get(activate_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],'Invalid activation url')

    def test_verify_is_blocked(self):
        token = RefreshToken.for_user(self.test_user_blocked).access_token
        activate_link = reverse('email-activate')
        activate_url = activate_link + "?token=" + str(token)
        response = self.client.get(activate_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid activation url')