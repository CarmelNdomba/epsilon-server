from django.db import models
from .device import Device


class FileMetadata(models.Model):
    """
    Arbre virtuel des fichiers présents sur le téléphone.
    """

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='files')

    path = models.TextField(db_index=True)  # /storage/emulated/0/Download/file.pdf
    name = models.CharField(max_length=255)
    is_dir = models.BooleanField(default=False)

    size = models.BigIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=128, null=True, blank=True)

    last_modified = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["device", "path"]),
            models.Index(fields=["device", "is_dir"]),
        ]
        unique_together = ('device', 'path')

    def __str__(self):
        return self.path
