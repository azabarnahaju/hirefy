"""
Tests for job API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Job
from core.enums import Seniority, Employment, Role
from core.utils import get_or_create_language_skills

from job.serializers import (
    JobSerializer,
    JobDetailSerializer,
)


JOBS_URL = reverse('job:job-list')


def detail_url(job_id):
    """Create and return a job detail URL."""
    return reverse('job:job-detail', args=[job_id])


def create_job(company, **params):
    """Create and return a sample job."""
    defaults = {
        'title': 'Sample job title',
        'description': 'Sample job description',
        'main_tasks': 'Sample job main tasks',
        'min_salary': 50000,
        'max_salary': 150000,
        'seniority': Seniority.JUNIOR,
        'employment_type': Employment.FULL_TIME,
        'languages': [
            {
                'language': 'English',
                'level': 'Advanced'
            }
        ]
    }
    defaults.update(params)
    language_data = defaults.pop('languages')
    job = Job.objects.create(company=company, **defaults)

    for language in language_data:
        language_skill = get_or_create_language_skills(language)
        job.languages.add(language_skill)

    return job

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicJobAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(JOBS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.company_user = create_user(
            email='companyuser@test.com',
            password='testpass123',
            role=Role.COMPANY
        )

        self.client.force_authenticate(self.company_user)

    def test_retrieve_jobs(self):
        """Test retrieving a list of jobs."""
        create_job(company=self.company_user)
        create_job(company=self.company_user)

        res = self.client.get(JOBS_URL)

        jobs = Job.objects.all().order_by('-id')
        serializer = JobSerializer(jobs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_job_detail(self):
        """Test get job detail."""
        job = create_job(company=self.company_user)

        url = detail_url(job.id)
        res = self.client.get(url)

        serializer = JobDetailSerializer(job)
        self.assertEqual(res.data, serializer.data)

    def test_create_job(self):
        """Test creating a job."""
        payload = {
            'title': 'Sample job title',
            'description': 'Sample job description',
            'main_tasks': 'Sample job main tasks',
            'min_salary': 50000,
            'max_salary': 150000,
            'seniority': Seniority.JUNIOR,
            'employment_type': Employment.FULL_TIME,
            'languages' : [
                {
                    'language': 'English',
                    'level': 'Beginner'
                }
            ]
        }
        res = self.client.post(JOBS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        job = Job.objects.get(id=res.data['id'])
        payload.pop('languages')
        for k, v in payload.items():
            self.assertEqual(getattr(job, k), v)
        self.assertEqual(job.company, self.company_user)

    def test_partial_update(self):
        """Test partial update of a job."""
        original_title = 'Sample job title'
        job = create_job(
            company=self.company_user,
            title=original_title,
            description='Sample job description'
        )

        payload = {
            'title': 'New job title'
        }
        url = detail_url(job.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        self.assertEqual(job.title, payload['title'])
        self.assertEqual(job.description, 'Sample job description')
        self.assertEqual(job.company, self.company_user)

    def test_full_update(self):
        """Test full update of job."""
        job = create_job(company=self.company_user)
        payload = {
            'title': 'New job title',
            'description': 'New job description',
            'main_tasks': 'New job main tasks',
            'min_salary': 60000,
            'max_salary': 160000,
            'seniority': Seniority.SENIOR,
            'employment_type': Employment.CONTRACT,
            'languages': [
                {
                    'language': 'English',
                    'level': 'Advanced'
                }
            ]
        }
        url = detail_url(job.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        payload.pop('languages')

        for k, v in payload.items():
            self.assertEqual(getattr(job, k), v)

        self.assertEqual(job.company, self.company_user)

    def test_full_update_to_empty_languages_success(self):
        """Test full update of job when updating to empty languages."""
        job = create_job(company=self.company_user)
        payload = {
            'title': 'New job title',
            'description': 'New job description',
            'main_tasks': 'New job main tasks',
            'min_salary': 60000,
            'max_salary': 160000,
            'seniority': Seniority.SENIOR,
            'employment_type': Employment.CONTRACT,
            'languages': []
        }
        url = detail_url(job.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        payload.pop('languages')
        for k, v in payload.items():
            self.assertEqual(getattr(job, k), v)
        self.assertEqual(job.company, self.company_user)

    def test_update_user_returns_error(self):
        """Test changing the job company results in an error."""
        new_user = create_user(email='another_user@test.com', password='test123', role=Role.TALENT)
        job = create_job(company=self.company_user)

        payload = {
            'company': new_user
        }

        url = detail_url(job.id)
        self.client.patch(url, payload)

        job.refresh_from_db()
        self.assertEqual(job.company, self.company_user)

    def test_delete_job(self):
        """Test deleting a job successful."""
        job = create_job(company=self.company_user)

        url = detail_url(job.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Job.objects.filter(id=job.id).exists())

    def test_delete_other_users_job_error(self):
        """Test trying to delete another company's job gives error."""
        new_user = create_user(email='another_user@test.com', password='test123', role=Role.COMPANY)
        job = create_job(company=new_user)

        url = detail_url(job.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Job.objects.filter(id=job.id).exists())
