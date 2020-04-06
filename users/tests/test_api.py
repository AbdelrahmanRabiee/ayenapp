from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()


class TestUserAPI(APITestCase):
    def setUp(self):
        self.sign_up_url = '/api/v1/user/'
        self.update_profile_url = '/api/v1/user/update_profile/'
        self.existing_user = User.objects.create_user(
            email='existing@localhost.com',
            password='goodpass123'
        )

        

    def test_user_can_signup(self):
        """Test user can signup with email and password"""
        data = {
            'email': 'abdelrahman.sico@gmail.com',
            'password': '$omethingHardtoknow123',
        }

        resp = self.client.post(self.sign_up_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email=data['email']).count(), 1)


    def test_user_cant_signup_with_existing_email(self):
        """
        check that user cant signup with existing email
        """
        data = {
            'email': 'existing@localhost.com',
            'password': '$omethingHardtoknow123',
        }

        resp = self.client.post(self.sign_up_url, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_signup_with_common_password(self):
        """
        check that user cant signup with common passwod easy to guess
        """
        data = {
            'email': 'abdelrahman@gmail.com',
            'password': '12345678',
        }

        resp = self.client.post(self.sign_up_url, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_can_update_profile(self):
        """
        check that user can update his profile info 
        """
        self.client.force_login(self.existing_user)
        data = {
            'name': 'abdulrahman rabiee',
        }

        resp = self.client.post(self.update_profile_url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'abdulrahman rabiee') 