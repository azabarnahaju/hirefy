"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.enums import Role


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        role = Role.ADMIN
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)
        self.assertEqual(user.role, role)

    def test_new_user_normalized_email(self):
        """Test email is normalized for new user."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                'sample123',
                Role.TALENT
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises an error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                'test123',
                Role.ADMIN
            )

    def test_new_user_without_role_raises_error(self):
        """Test that creating a user without a role
        or an incorrect role raises an error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'test@example.com',
                'test123',
                ''
            )

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'test@example.com',
                'test123',
                "CANDIDATE"
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.ADMIN

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)
        self.assertEqual(user.role, role)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
