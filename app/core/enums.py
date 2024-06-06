"""
Enums for choice fields.
"""
from django.db import models


class Role(models.TextChoices):
    """User roles."""
    ADMIN = "ADMIN", 'Admin'
    COMPANY = "COMPANY", 'Company'
    TALENT = "TALENT", 'Talent'
