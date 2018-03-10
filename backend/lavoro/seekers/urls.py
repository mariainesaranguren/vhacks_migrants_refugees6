from rest_framework import status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from seekers.views import SeekerViewSet

router = DefaultRouter()
router.register(r'', SeekerViewSet, base_name='user')
urlpatterns = router.urls