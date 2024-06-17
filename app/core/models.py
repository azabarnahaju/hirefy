"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from core.enums import Role, Seniority, Employment


class UserManager(BaseUserManager):
    """Manager for base users."""

    def create_user(self, email, password=None, role=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('The email field must be set.')
        if not role:
            raise ValueError('Role must be set.')
        if role not in [choice[0] for choice in Role.choices]:
            raise ValueError('Invalid role.')

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, role=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        role = Role.ADMIN
        return self.create_user(email, password, role, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Base user in the system."""

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=255, choices=Role.choices)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class CompanyProfile(models.Model):
    """Company profile for users wit company role."""
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )
    name = models.CharField(max_length=255)

    def clean(self, *args, **kwargs):
        if self.account.role != Role.COMPANY:
            raise ValidationError("Invalid role for this profile type")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"COMPANY | {self.name}"


class TalentProfile(models.Model):
    """Profile for talent users."""
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='talent_profile'
    )
    profile_description = models.TextField()

    def clean(self, *args, **kwargs):
        if self.account.role != Role.TALENT:
            raise ValidationError("Invalid role for this profile type")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TALENT | {self.account.get_full_name()}"


class Job(models.Model):
    """Job object."""
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_tasks = models.TextField()
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    seniority = models.CharField(
        max_length=255,
        choices=Seniority.choices
    )
    employment_type = models.CharField(
        max_length=255,
        choices=Employment.choices
    )

    def clean(self, *args, **kwargs):
        if self.company.role != Role.COMPANY:
            raise ValidationError("Only companies can have jobs.")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
