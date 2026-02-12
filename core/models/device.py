from django.db import models
import uuid


class Device(models.Model):
    """
    Représente un téléphone Android connecté au serveur.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device_uid = models.CharField(max_length=128, unique=True, db_index=True)
    code = models.CharField(max_length=32, unique=True, blank=True, null=True) 
    name = models.CharField(max_length=128, blank=True, null=True)
    manufacturer = models.CharField(max_length=128, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    android_version = models.CharField(max_length=32, blank=True, null=True)

    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_user_agent = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["device_uid"]),
            models.Index(fields=["is_online"]),
        ]
        ordering = ["-last_seen"]

    def __str__(self):
        return f"{self.name or 'Android'} [{self.device_uid[:8]}]"


class DeviceConnectionLog(models.Model):
    """
    Historique complet des connexions / déconnexions.
    """

    STATUS_CHOICES = (
        ('connected', 'Connected'),
        ('disconnected', 'Disconnected'),
    )

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
