"""
Utility functions.
"""

from .models import LanguageSkill


def get_or_create_language_skills(language_data):
    language_skill, created = LanguageSkill.objects.get_or_create(
        language=language_data['language'],
        level=language_data['level']
    )
    return language_skill
