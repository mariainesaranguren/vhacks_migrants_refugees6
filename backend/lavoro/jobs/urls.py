from rest_framework import status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from jobs.views import JobsViewSet

router = DefaultRouter()
router.register(r'', JobsViewSet, base_name='jobs')
urlpatterns = router.urls