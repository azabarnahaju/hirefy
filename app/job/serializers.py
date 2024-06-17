"""
Serializers for job APIs.
"""
from rest_framework import serializers

from core.models import Job


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobs."""

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'seniority']
        read_only_fields = ['id']


class JobDetailSerializer(JobSerializer):
    """Serializer for job detail view."""

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + ['employment_type', 'main_tasks', 'min_salary', 'max_salary']
        