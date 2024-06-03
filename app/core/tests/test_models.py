"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import User


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        role = User.Role.ADMIN
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)
        self.assertEqual(user.role, role)
