"""
Utility functions.
"""

from .models import (
    LanguageSkill,
    TechnicalSkill,
    PersonalSkill
)


def get_or_create_language_skills(language_data):
    language_skill, created = LanguageSkill.objects.get_or_create(
        language=language_data['language'],
        level=language_data['level']
    )
    return language_skill


def get_or_create_technical_skills(tech_skill_data):
    tech_skill, created = TechnicalSkill.objects.get_or_create(
        value=tech_skill_data['value']
    )
    return tech_skill


def get_or_create_personal_skills(pers_skill_data):
    pers_skill, created = PersonalSkill.objects.get_or_create(
        value=pers_skill_data['value']
    )
    return pers_skill
