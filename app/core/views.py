"""
Views for the enum objects.
"""
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from .enums import (
    LangProf,
    LangSkill,
    TechSkill,
    PersSkill
)
from .serializers import (
    LanguageLevelSerializer,
    LanguageSerializer,
    TechnicalSkillEnumSerializer,
    PersonalSkillEnumSerializer
)


class LangSkillListView(GenericAPIView, ListModelMixin):
    """View for listing all the languages."""
    serializer_class = LanguageSerializer

    def get(self, request, *args, **kwargs):
        choices = LangSkill.choices
        data = [{'value': choice[0], 'label': choice[1]} for choice in choices]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class LangProfListView(GenericAPIView, ListModelMixin):
    """View for listing all the language levels."""
    serializer_class = LanguageLevelSerializer

    def get(self, request, *args, **kwargs):
        choices = LangProf.choices
        data = [{'value': choice[0], 'label': choice[1]} for choice in choices]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class TechSkillListView(GenericAPIView, ListModelMixin):
    """View for listing all the technical skills."""
    serializer_class = TechnicalSkillEnumSerializer

    def get(self, request, *args, **kwargs):
        choices = TechSkill.choices
        data = [{'value': choice[0], 'label': choice[1]} for choice in choices]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class PersSkillListView(GenericAPIView, ListModelMixin):
    """View for listing all the personal skills."""
    serializer_class = PersonalSkillEnumSerializer

    def get(self, request, *args, **kwargs):
        choices = PersSkill.choices
        data = [{'value': choice[0], 'label': choice[1]} for choice in choices]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)
