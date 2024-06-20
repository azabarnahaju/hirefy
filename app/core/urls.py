"""
Endpoints for the enum objects.
"""
from django.urls import path

from .views import (
    LangSkillListView,
    LangProfListView
)

urlpatterns = [
    path('languages', LangSkillListView.as_view(), name='language-list'),
    path('language-levels', LangProfListView.as_view(), name='language-levels')
]