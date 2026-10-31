from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class AccountsTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'priya',
            'first_name': 'Priya',
            'last_name': 'Mehta',
            'email': 'priya@example.com',
            'password1': 'SecurePass@123',
            'password2': 'SecurePass@123',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(username='priya').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'priya@example.com')
        # Check automatic profile creation signal
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_user_login_and_logout(self):
        User.objects.create_user(username='vikram', email='vikram@example.com', password='Password@123')
        # Login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'vikram',
            'password': 'Password@123',
        })
        self.assertEqual(response.status_code, 302)
        # Logout
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_update(self):
        user = User.objects.create_user(username='kavita', email='kavita@example.com', password='Password@123')
        self.client.login(username='kavita', password='Password@123')
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Kavita',
            'last_name': 'Sharma',
            'email': 'kavita.updated@example.com',
            'phone': '9876543210',
            'address_line1': '101 Rose Garden',
            'address_line2': 'Near Metro',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pin_code': '400001',
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.email, 'kavita.updated@example.com')
        self.assertEqual(user.profile.city, 'Mumbai')
