"""
Tests for the enum API.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


LANGUAGES_URL = reverse('language-list')
LANGUAGE_LEVEL_URL = reverse('language-levels')


class EnumTests(TestCase):
    """Test enums."""

    def setUp(self):
        self.client = APIClient()

    def test_get_method_returns_langages(self):
        """Test that a GET method returns all the languages."""
        res = self.client.get(LANGUAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_method_returns_language_levels(self):
        """Test that a GET method returns all the language levels."""
        res = self.client.get(LANGUAGE_LEVEL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
