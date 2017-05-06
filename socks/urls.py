from rest_framework.routers import DefaultRouter

from socks import viewsets

router = DefaultRouter()
router.register(r'socks', viewsets.SockViewSet)
router.register(r'sock-preferences', viewsets.SockPreferenceViewSet)

urlpatterns = router.urls
