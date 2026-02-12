from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models.files import FileMetadata
from core.models.device import Device
from core.serializers import FileMetadataSerializer

class FileMetadataViewSet(viewsets.ViewSet):
    """
    Endpoint pour créer ou lister les fichiers d'un device.
    """

    @action(detail=False, methods=['post'], url_path='create')
    def create_file(self, request):
        device_uid = request.data.get('device')
        if not device_uid:
            return Response({"error": "device is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(device_uid=device_uid)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['device'] = device.id  # sérializer attend l'id PK

        serializer = FileMetadataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "file": serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
