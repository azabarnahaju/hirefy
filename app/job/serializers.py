"""
Serializers for job APIs.
"""
from rest_framework import serializers

from core.models import Job
from core.utils import (
    get_or_create_language_skills,
    get_or_create_technical_skills,
    get_or_create_personal_skills
)
from core.serializers import (
    LanguageSkillSerializer,
    TechnicalSkillSerializer,
    PersonalSkillSerializer
)


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobs."""
    languages = LanguageSkillSerializer(
        many=True,
        required=False
    )
    technical_skills = TechnicalSkillSerializer(
        many=True,
        required=False
    )
    personal_skills = PersonalSkillSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'seniority', 'languages',
            'technical_skills', 'personal_skills'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        language_data = validated_data.pop('languages', [])
        tech_skill_data = validated_data.pop('technical_skills', [])
        pers_skill_data = validated_data.pop('personal_skills', [])
        job = Job.objects.create(**validated_data)

        for data in language_data:
            language_skill = get_or_create_language_skills(data)
            job.languages.add(language_skill)

        for data in tech_skill_data:
            tech_skill = get_or_create_technical_skills(data)
            job.technical_skills.add(tech_skill)

        for data in pers_skill_data:
            pers_skill = get_or_create_personal_skills(data)
            job.personal_skills.add(pers_skill)

        return job

    def update(self, instance, validated_data):
        if validated_data.get('languages'):
            instance.languages.clear()
        if validated_data.get('technical_skills'):
            instance.technical_skills.clear()
        if validated_data.get('personal_skills'):
            instance.personal_skills.clear()
        language_data = validated_data.pop('languages', [])
        tech_skill_data = validated_data.pop('technical_skills', [])
        pers_skill_data = validated_data.pop('personal_skills', [])
        instance = super().update(instance, validated_data)

        for data in language_data:
            language_skill = get_or_create_language_skills(data)
            instance.languages.add(language_skill)

        for data in tech_skill_data:
            tech_skill = get_or_create_technical_skills(data)
            instance.technical_skills.add(tech_skill)

        for data in pers_skill_data:
            pers_skill = get_or_create_personal_skills(data)
            instance.personal_skills.add(pers_skill)

        instance.save()
        return instance


class JobDetailSerializer(JobSerializer):
    """Serializer for job detail view."""

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + [
            'employment_type', 'main_tasks',
            'min_salary', 'max_salary'
        ]
