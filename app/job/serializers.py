"""
Serializers for job APIs.
"""
from rest_framework import serializers

from core.models import Job
from core.utils import get_or_create_language_skills
from core.serializers import LanguageSkillSerializer


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobs."""
    languages = LanguageSkillSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'seniority', 'languages']
        read_only_fields = ['id']

    def create(self, validated_data):
        language_data = validated_data.pop('languages', [])
        job = Job.objects.create(**validated_data)

        for data in language_data:
            language_skill = get_or_create_language_skills(data)
            job.languages.add(language_skill)

        return job

    def update(self, instance, validated_data):
        language_data = validated_data.pop('languages', [])
        instance = super().update(instance, validated_data)
        instance.languages.clear()

        for data in language_data:
            language_skill = get_or_create_language_skills(data)
            instance.languages.add(language_skill)

        instance.save()
        return instance


class JobDetailSerializer(JobSerializer):
    """Serializer for job detail view."""

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + [
            'employment_type', 'main_tasks',
            'min_salary', 'max_salary'
        ]
