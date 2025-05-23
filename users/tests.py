from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }

    def test_user_registration(self):
        """Test user registration with valid data"""
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_registration_invalid_data(self):
        """Test user registration with invalid data"""
        invalid_data = {
            'username': '',  # Empty username
            'email': 'invalid-email',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test user login with valid credentials"""
        # First create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Try to login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials and missing fields"""
        # Wrong password (should return 401)
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Missing password (should return 400)
        missing_field_data = {
            'username': 'testuser'
        }
        response = self.client.post(self.login_url, missing_field_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_protected_endpoint(self):
        """Test accessing protected endpoint with and without authentication"""
        # Create a user and get token
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        token = login_response.data['access']

        # Test without authentication
        response = self.client.get(reverse('user-detail'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('user-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
