from rest_framework.routers import DefaultRouter
from .views import EmergencyViewSet

router = DefaultRouter()
router.register(r'', EmergencyViewSet, basename='emergencies')

urlpatterns = router.urls