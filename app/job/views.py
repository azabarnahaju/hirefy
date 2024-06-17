"""
Views for the job APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Job
from core.permissions import IsOwnerOfJob
from job import serializers


class JobViewSet(viewsets.ModelViewSet):
    """View for manage job APIs."""
    serializer_class = serializers.JobDetailSerializer
    queryset = Job.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwnerOfJob]

    def get_queryset(self):
        """Retrieve jobs for authenticated user."""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.JobSerializer
        return serializers.JobDetailSerializer

    def perform_create(self, serializer):
        """Create a new job."""
        serializer.save(company=self.request.user)