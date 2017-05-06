from rest_framework.routers import DefaultRouter

from users import viewsets

router = DefaultRouter()
router.register(r'', viewsets.UserViewSet)

urlpatterns = router.urls
