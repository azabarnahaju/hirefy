"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model as User
from django.core.exceptions import ValidationError

from core.enums import Role, Seniority, Employment
from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        role = Role.ADMIN
        user = User().objects.create_user(
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
            user = User().objects.create_user(
                email,
                'sample123',
                Role.TALENT
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises an error."""
        with self.assertRaises(ValueError):
            User().objects.create_user(
                '',
                'test123',
                Role.ADMIN
            )

    def test_new_user_without_role_raises_error(self):
        """Test that creating a user without a role
        or an incorrect role raises an error."""
        with self.assertRaises(ValueError):
            User().objects.create_user(
                'test@example.com',
                'test123',
                ''
            )

        with self.assertRaises(ValueError):
            User().objects.create_user(
                'test@example.com',
                'test123',
                "CANDIDATE"
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.ADMIN

        user = User().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)
        self.assertEqual(user.role, role)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_company_profile(self):
        """Test creating a company profile."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.COMPANY

        user = User().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        company_profile = models.CompanyProfile.objects.create(
            account=user,
            name="Test Company"
        )

        self.assertEqual(company_profile.account.email, email)
        self.assertEqual(company_profile.name, "Test Company")
        self.assertEqual(str(company_profile),
                         f"COMPANY | {company_profile.name}")

    def test_create_company_profile_wrong_role_raise_error(self):
        """Test creating a company profile with wrong role
            returns ValidationError."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.TALENT

        user = User().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        with self.assertRaises(ValidationError):
            models.CompanyProfile.objects.create(
                account=user,
                name="Test Company"
            )

    def test_create_talent_profile(self):
        """Test creating a company profile."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.TALENT

        user = User().objects.create_user(
            email=email,
            password=password,
            role=role
        )
        talent_profile = models.TalentProfile.objects.create(
            account=user,
            profile_description="Test Description"
        )

        self.assertEqual(talent_profile.account.email, email)
        self.assertEqual(talent_profile.profile_description,
                         "Test Description")

    def test_create_talent_profile_wrong_role_raise_error(self):
        """Test creating a talent profile with company role
        returns ValidationError."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.COMPANY

        user = User().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        with self.assertRaises(ValidationError):
            models.TalentProfile.objects.create(
                account=user,
                profile_description="Test Description"
            )

    def test_create_job_successful_company(self):
        """Test creating a job works only with company role owner."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.COMPANY

        user = User().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        job = models.Job.objects.create(
            company=user,
            title="Test Title",
            description="Test Description",
            main_tasks='Test Task #1',
            min_salary=50000,
            max_salary=150000,
            seniority=Seniority.JUNIOR,
            employment_type=Employment.FULL_TIME
        )

        self.assertEqual(job.company.email, email)
        self.assertEqual(job.title, "Test Title")
        self.assertEqual(job.seniority, Seniority.JUNIOR)
        self.assertEqual(job.min_salary, 50000)
        self.assertEqual(job.description, "Test Description")

    def test_create_job_not_company_owner_raises_error(self):
        """Test creating a job with not company role
            owner raises ValidationError."""
        email = 'test@example.com'
        password = 'test123'
        role = Role.TALENT

        user = User().objects.create_user(
            email=email,
            password=password,
            role=role
        )

        with self.assertRaises(ValidationError):
            models.Job.objects.create(
                company=user,
                title="Test Title",
                description="Test Description",
                main_tasks='Test Task #1',
                min_salary=50000,
                max_salary=150000,
                seniority=Seniority.JUNIOR,
                employment_type=Employment.FULL_TIME
            )
