"""
Endpoints for the enum objects.
"""
from django.urls import path

from .views import (
    LangSkillListView,
    LangProfListView,
    TechSkillListView,
    PersSkillListView
)

urlpatterns = [
    path('languages', LangSkillListView.as_view(), name='language-list'),
    path('language-levels',
         LangProfListView.as_view(),
         name='language-levels'),
    path('technical-skills',
         TechSkillListView.as_view(),
         name='technical-skills'),
    path('personal-skills',
         PersSkillListView.as_view(),
         name='personal-skills')
]
