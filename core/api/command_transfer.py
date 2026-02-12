# core/api/command_transfer.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models.device import Device
from core.models.command import Command
from core.models.transfer import FileTransfer
from core.serializers import CommandSerializer, FileTransferSerializer


# -----------------------------
# Command ViewSet
# -----------------------------
class CommandViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour créer, lister et mettre à jour des commandes.
    """
    queryset = Command.objects.all().order_by('-created_at')
    serializer_class = CommandSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Créer une commande pour un device
        Body JSON attendu:
        {
            "device": "ABC123456",
            "command_type": "SCAN",
            "payload": {...}
        }
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='pending')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Mettre à jour le status ou le résultat d'une commande
        Body JSON exemple:
        {
            "status": "done",
            "result": {...},
            "error_message": ""
        }
        """
        try:
            command = Command.objects.get(pk=pk)
        except Command.DoesNotExist:
            return Response({"detail": "Command not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(command, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# FileTransfer ViewSet
# -----------------------------
class FileTransferViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour suivre l'état des transferts de fichiers.
    """
    queryset = FileTransfer.objects.all().order_by('-created_at')
    serializer_class = FileTransferSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Créer un suivi de transfert pour un fichier
        Body JSON attendu:
        {
            "device": "ABC123456",
            "command": 12,  # ID de la commande associée
            "file_path": "/storage/emulated/0/Download/test.pdf",
            "file_size": 12345
        }
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='pending', progress=0.0)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='update-progress')
    def update_progress(self, request, pk=None):
        """
        Mettre à jour le progrès ou le status d'un transfert
        Body JSON exemple:
        {
            "status": "running",
            "progress": 45.5
        }
        """
        try:
            transfer = FileTransfer.objects.get(pk=pk)
        except FileTransfer.DoesNotExist:
            return Response({"detail": "FileTransfer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(transfer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
