from django.contrib import admin
from django.utils.html import format_html
from core.models.device import Device, DeviceConnectionLog
from core.models.files import FileMetadata
from core.models.command import Command
from core.models.transfer import FileTransfer

# -------------------------
# Inlines pour Device
# -------------------------
class DeviceConnectionLogInline(admin.TabularInline):
    model = DeviceConnectionLog
    extra = 0
    readonly_fields = ('status_colored', 'ip_address', 'user_agent', 'timestamp')
    can_delete = False

    def status_colored(self, obj):
        color = "green" if obj.status == "connected" else "red"
        return format_html('<b><span style="color:{}">{}</span></b>', color, obj.status)
    status_colored.short_description = "Status"

class CommandInline(admin.TabularInline):
    model = Command
    extra = 0
    readonly_fields = ('command_type', 'status_colored', 'issued_by', 'created_at', 'executed_at', 'finished_at')
    show_change_link = True

    def status_colored(self, obj):
        colors = {
            "pending": "orange",
            "sent": "blue",
            "running": "purple",
            "done": "green",
            "failed": "red"
        }
        color = colors.get(obj.status, "black")
        return format_html('<b><span style="color:{}">{}</span></b>', color, obj.status)
    status_colored.short_description = "Status"

class FileMetadataInline(admin.TabularInline):
    model = FileMetadata
    extra = 0
    readonly_fields = ('path', 'name', 'is_dir', 'size', 'mime_type', 'last_modified')

class FileTransferInline(admin.TabularInline):
    model = FileTransfer
    extra = 0
    readonly_fields = ('file_path', 'file_size', 'status_colored', 'progress', 'created_at', 'finished_at')

    def status_colored(self, obj):
        colors = {
            "pending": "orange",
            "running": "purple",
            "done": "green",
            "failed": "red"
        }
        color = colors.get(obj.status, "black")
        return format_html('<b><span style="color:{}">{}</span></b>', color, obj.status)
    status_colored.short_description = "Status"


# -------------------------
# Device admin
# -------------------------
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_uid', 'name', 'manufacturer', 'model', 'android_version', 'is_online_colored', 'last_seen')
    search_fields = ('device_uid', 'name', 'manufacturer', 'model')
    list_filter = ('is_online', 'manufacturer', 'android_version')
    readonly_fields = ('id', 'last_seen', 'created_at')

    inlines = [DeviceConnectionLogInline, CommandInline, FileMetadataInline, FileTransferInline]

    def is_online_colored(self, obj):
        color = "green" if obj.is_online else "red"
        status = "Online" if obj.is_online else "Offline"
        return format_html('<b><span style="color:{}">{}</span></b>', color, status)
    is_online_colored.short_description = "Status"
