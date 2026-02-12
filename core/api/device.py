# core/api/device.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.models.device import Device, DeviceConnectionLog
from core.models.files import FileMetadata
from core.models.command import Command
from core.models.transfer import FileTransfer

from core.serializers import (
    DeviceRegisterSerializer,
    FileMetadataSerializer,
    CommandSerializer,
    FileTransferSerializer,
    DeviceConnectionLogSerializer,
)


# ----------------------
# Device registration
# ----------------------
class DeviceRegisterAPIView(APIView):
    """
    Endpoint pour enregistrer ou mettre à jour un device Android.
    """

    def _get_device(self, identifier):
        """
        Récupère un device soit par device_uid (UUID) soit par code simple.
        """
        try:
            return Device.objects.get(device_uid=identifier)
        except (Device.DoesNotExist, ValueError):
            try:
                return Device.objects.get(code=identifier)
            except Device.DoesNotExist:
                return None

    def post(self, request):
        device_identifier = request.data.get('device_uid')
        if not device_identifier:
            return Response({"error": "device_uid is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Cherche le device par UUID ou code
        device = self._get_device(device_identifier)
        created = False
        if not device:
            # Crée un nouveau device avec un device_uid généré si aucun UUID fourni
            device = Device.objects.create(device_uid=device_identifier, code=device_identifier)
            created = True

        # Met à jour les infos du device
        serializer = DeviceRegisterSerializer(device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_online=True)
            return Response({"success": True, "device": serializer.data, "created": created})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------
# Device REST endpoints
# ----------------------
class DeviceFileViewSet(viewsets.ViewSet):
    """
    Endpoints pour gérer les fichiers, commandes, transferts et status d'un device.
    """

    permission_classes = [IsAuthenticated]

    def _get_device(self, identifier):
        """
        Récupère un device soit par device_uid (UUID) soit par code simple.
        """
        try:
            return Device.objects.get(device_uid=identifier)
        except (Device.DoesNotExist, ValueError):
            try:
                return Device.objects.get(code=identifier)
            except Device.DoesNotExist:
                return None

    # Lister les fichiers
    @action(detail=True, methods=['get'], url_path='files')
    def list_files(self, request, pk=None):
        device = self._get_device(pk)
        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        path_filter = request.query_params.get('path', None)
        files = FileMetadata.objects.filter(device=device)
        if path_filter:
            files = files.filter(path__startswith=path_filter)

        serializer = FileMetadataSerializer(files, many=True)
        return Response(serializer.data)

    # Créer une commande
    @action(detail=True, methods=['post'], url_path='command')
    def create_command(self, request, pk=None):
        device = self._get_device(pk)
        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device=device, status='pending', issued_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mettre à jour un transfert
    @action(detail=True, methods=['post'], url_path='transfer')
    def update_transfer(self, request, pk=None):
        device = self._get_device(pk)
        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        command_id = request.data.get('command_id')
        try:
            command = Command.objects.get(id=command_id, device=device)
        except Command.DoesNotExist:
            return Response({"detail": "Command not found"}, status=status.HTTP_404_NOT_FOUND)

        transfer, created = FileTransfer.objects.get_or_create(command=command, defaults={'device': device})
        serializer = FileTransferSerializer(transfer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mettre à jour le statut du device
    @action(detail=True, methods=['post'], url_path='status')
    def update_status(self, request, pk=None):
        device = self._get_device(pk)
        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceConnectionLogSerializer(data=request.data)
        if serializer.is_valid():
            log = serializer.save(device=device)
            # Mettre à jour le device
            device.is_online = (log.status == 'connected')
            device.last_ip = log.ip_address
            device.last_user_agent = log.user_agent
            device.save(update_fields=['is_online', 'last_ip', 'last_user_agent', 'last_seen'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
