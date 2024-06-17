"""
URL mappings for the job app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from job import views


router = DefaultRouter()
router.register('jobs', views.JobViewSet)

app_name = 'job'

urlpatterns = [
    path('', include(router.urls))
]