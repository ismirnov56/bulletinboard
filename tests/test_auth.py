from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsTestAuth(APITestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(email='test@example.com', phone='+9(999)9999999',
                                                              password='testpassword159789')
        self.test_user.is_verify = True
        self.test_user.is_active = True
        self.test_user.save()
        self.test_staff = get_user_model().objects.create_stuff_user(email='staff@example.com', phone='+8(999)9999999',
                                                                     password='testpassword159789')
        self.test_staff.is_verify = True
        self.test_staff.is_active = True
        self.test_staff.save()
        self.test_admin = get_user_model().objects.create_superuser(email='admin@example.com',
                                                                    phone='+7(777)7777777',
                                                                    password='testpassword159789')
        self.login_url = reverse('token-login')

    def test_auth_admin(self):
        data = {
            'email': 'admin@example.com',
            'password': 'testpassword159789'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('email' in response.data)
        self.assertTrue('access' in response.data)
        self.assertTrue(response.data['is_staff'])
        self.assertTrue(response.data['is_admin'])

    def test_auth_staff(self):
        data = {
            'email': 'staff@example.com',
            'password': 'testpassword159789'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('email' in response.data)
        self.assertTrue('access' in response.data)
        self.assertTrue(response.data['is_staff'])
        self.assertFalse(response.data['is_admin'])

    def test_auth_user(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword159789'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('email' in response.data)
        self.assertTrue('access' in response.data)
        self.assertFalse(response.data['is_staff'])
        self.assertFalse(response.data['is_admin'])

    def test_auth_bad_user_email(self):
        data = {
            'email': 'testasd@example.com',
            'password': 'testpassword159789'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],
                         'Invalid credentials, try again')

    def test_auth_bad_user_password(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],
                         'Invalid credentials, try again')

    def test_auth_bad_no_verify(self):
        get_user_model().objects.create_user(email='testautbadverify@example.com', phone='+2(999)9999999',
                                             password='testpassword159789')
        data = {
            'email': 'testautbadverify@example.com',
            'password': 'testpassword159789'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],
                         'User is not verify, please activate your account with email or contact Admin')

    def test_auth_bad_no_active(self):
        test_user = get_user_model().objects.create_user(email='testautbadactive@example.com', phone='+3(999)9999999',
                                                         password='testpassword159789')
        test_user.is_verify = True
        test_user.save()
        data = {
            'email': 'testautbadactive@example.com',
            'password': 'testpassword159789'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],
                         'User is blocked, contact Admin')
