from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.profiles.models import BBUser


class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(email='test@example.com', phone='+9(999)9999999',
                                                    password='testpassword159789')
        self.test_admin = get_user_model().objects.create_superuser(email='admin@example.com',
                                                                    phone='+7(777)7777777',
                                                                    password='testpassword159789')
        self.create_url = reverse('account-create')

    """
    def test_create_user(self):
        data = {
            'email': 'test1@example.com',
            'phone': '+7(999)9999999',
            'password': 'somepassword159753'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BBUser.objects.count(), 3)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['phone'], data['phone'])
        self.assertFalse('password' in response.data)
    """

    def test_create_user_with_no_password(self):
        data = {
            'email': 'test2@example.com',
            'phone': '+7(909)9999999',
            'password': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('password' in response.data)

    def test_create_user_with_no_email(self):
        data = {
            'email': '',
            'phone': '+7(901)9999999',
            'password': 'noemail159753'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('email' in response.data)



    def test_create_user_with_no_phone(self):
        data = {
            'email': 'test3@example.com',
            'phone': '',
            'password': 'nophone1478995'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('phone' in response.data)

    def test_create_user_with_bad_email(self):
        data = {
            'email': 'test2',
            'phone': '+7(907)9999999',
            'password': 'bademail12578951'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('email' in response.data)

    def test_create_user_with_no_unique_email(self):
        data = {
            'email': 'test@example.com',
            'phone': '+7(904)9999999',
            'password': 'nouniqeemail12578951'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('email' in response.data)

    def test_create_user_with_bad_phone(self):
        data = {
            'email': 'test4@example.com',
            'phone': '+79079999999',
            'password': 'badphone12578951'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('phone' in response.data)

    def test_create_user_with_no_unique_phone(self):
        data = {
            'email': 'test5@example.com',
            'phone': '+9(999)9999999',
            'password': 'nouniqephone12578951'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BBUser.objects.count(), 2)
        self.assertTrue('phone' in response.data)