"""
Serializers for the enum objects.
"""
from rest_framework import serializers

from .models import LanguageSkill


class LanguageSerializer(serializers.Serializer):
    """Serializer for the language skill enum."""
    value = serializers.CharField()
    label = serializers.CharField()


class LanguageLevelSerializer(serializers.Serializer):
    """Serializer for the language level enum."""
    value = serializers.CharField()
    label = serializers.CharField()


class LanguageSkillSerializer(serializers.ModelSerializer):
    """Serializer for the the LanguageSkill model."""

    class Meta:
        model = LanguageSkill
        fields = ['language', 'level']
