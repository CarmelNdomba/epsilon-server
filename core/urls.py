# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api.device import DeviceRegisterAPIView, DeviceFileViewSet
from core.api.command_transfer import CommandViewSet, FileTransferViewSet
from core.api.files import FileMetadataViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Route pour les ViewSets
router = DefaultRouter()
router.register(r'device', DeviceFileViewSet, basename='device-files')
router.register(r'files', FileMetadataViewSet, basename='files')
router.register(r'commands', CommandViewSet, basename='commands')
router.register(r'transfers', FileTransferViewSet, basename='transfers')

urlpatterns = [
    # Endpoint pour enregistrer / mettre à jour un device
    path('device/register/', DeviceRegisterAPIView.as_view(), name='device-register'),

    # Endpoints JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Tous les endpoints des ViewSets via router
    path('', include(router.urls)),
]
