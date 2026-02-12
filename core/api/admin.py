from django.contrib import admin
from core.models.device import Device, DeviceConnectionLog
from core.models.files import FileMetadata
from core.models.command import Command
from core.models.transfer import FileTransfer

# -------------------------
# Inlines pour Device
# -------------------------
class DeviceConnectionLogInline(admin.TabularInline):
    model = DeviceConnectionLog
    extra = 0  # pas de lignes vides supplémentaires
    readonly_fields = ('status', 'ip_address', 'user_agent', 'timestamp')
    can_delete = False

class CommandInline(admin.TabularInline):
    model = Command
    extra = 0
    readonly_fields = ('command_type', 'status', 'issued_by', 'created_at', 'executed_at', 'finished_at')
    show_change_link = True  # permet d'aller dans le détail de la commande

class FileMetadataInline(admin.TabularInline):
    model = FileMetadata
    extra = 0
    readonly_fields = ('path', 'name', 'is_dir', 'size', 'mime_type', 'last_modified')

class FileTransferInline(admin.TabularInline):
    model = FileTransfer
    extra = 0
    readonly_fields = ('file_path', 'file_size', 'status', 'progress', 'created_at', 'finished_at')
