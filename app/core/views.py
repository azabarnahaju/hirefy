"""
Views for the enum objects.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from .enums import (
    LangProf,
    LangSkill
)
from .serializers import (
    LanguageLevelSerializer,
    LanguageSerializer
)


class LangSkillListView(APIView):
    """View for listing all the languages."""
    def get(self, request):
        choices = LangSkill.choices
        data = [{'value': choice[0], 'label': choice[1]} for choice in choices]
        serializer = LanguageSerializer(data, many=True)
        return Response(serializer.data)


class LangProfListView(APIView):
    """View for listing all the language levels."""
    def get(self, request):
        choices = LangProf.choices
        data = [{'value': choice[0], 'label': choice[1]} for choice in choices]
        serializer = LanguageLevelSerializer(data, many=True)
        return Response(serializer.data)
