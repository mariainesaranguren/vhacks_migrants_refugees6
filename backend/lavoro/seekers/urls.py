from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

class SeekerViewSet(viewsets.ViewSet):
    def create(self, request):
        return Response({}, status=status.HTTP_201_CREATED)

router = DefaultRouter()
router.register(r'', SeekerViewSet, base_name='user')
urlpatterns = router.urls