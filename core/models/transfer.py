from django.db import models
from .device import Device
from .command import Command


class FileTransfer(models.Model):
    """
    Suivi du téléchargement de fichiers.
    """

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    )

    id = models.BigAutoField(primary_key=True)

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='transfers')
    command = models.OneToOneField(Command, on_delete=models.CASCADE, related_name='transfer')

    file_path = models.TextField()
    file_size = models.BigIntegerField(null=True, blank=True)

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending')
    progress = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
