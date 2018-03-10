from rest_framework import status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from job_history.views import JobHistoryViewSet

router = DefaultRouter()
router.register(r'', JobHistoryViewSet, base_name='history')
urlpatterns = router.urls