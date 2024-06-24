"""
Serializers for the enum objects.
"""
from rest_framework import serializers

from .models import (
    LanguageSkill,
    TechnicalSkill,
    PersonalSkill
)


class LanguageSerializer(serializers.Serializer):
    """Serializer for the language skill enum."""
    value = serializers.CharField()
    label = serializers.CharField()


class LanguageLevelSerializer(serializers.Serializer):
    """Serializer for the language level enum."""
    value = serializers.CharField()
    label = serializers.CharField()


class TechnicalSkillEnumSerializer(serializers.Serializer):
    """Serializer for the technical skills enum."""
    value = serializers.CharField()
    label = serializers.CharField()


class PersonalSkillEnumSerializer(serializers.Serializer):
    """Serializer for the personal skills enum."""
    value = serializers.CharField()
    label = serializers.CharField()


class LanguageSkillSerializer(serializers.ModelSerializer):
    """Serializer for the the LanguageSkill model."""

    class Meta:
        model = LanguageSkill
        fields = ['language', 'level']


class TechnicalSkillSerializer(serializers.ModelSerializer):
    """Serializer for the technical skill."""

    class Meta:
        model = TechnicalSkill
        fields = '__all__'


class PersonalSkillSerializer(serializers.ModelSerializer):
    """Serializer for the personal skill."""

    class Meta:
        model = PersonalSkill
        fields = '__all__'
