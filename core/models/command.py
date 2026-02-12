from django.db import models
from django.contrib.auth import get_user_model
from .device import Device

User = get_user_model()


class Command(models.Model):
    """
    Commande envoyée par l'admin vers un device.
    """

    COMMAND_TYPES = (
        ('SCAN', 'Scan filesystem'),
        ('LIST', 'List directory'),
        ('GET', 'Download file'),
        ('PING', 'Ping device'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    )

    id = models.BigAutoField(primary_key=True)

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    command_type = models.CharField(max_length=16, choices=COMMAND_TYPES)
    payload = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending')
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
