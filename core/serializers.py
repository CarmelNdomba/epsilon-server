# core/serializers.py

from rest_framework import serializers
from core.models.device import Device, DeviceConnectionLog
from core.models.files import FileMetadata
from core.models.command import Command
from core.models.transfer import FileTransfer


# ----------------------
# Device
# ----------------------
class DeviceRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id', 'device_uid', 'code','name', 'manufacturer', 'model',
            'android_version', 'is_online', 'last_seen', 'last_ip', 'last_user_agent'
        ]
        read_only_fields = ['id', 'is_online', 'last_seen']


# ----------------------
# FileMetadata
# ----------------------
class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = [
            'id', 'device', 'path', 'name', 'is_dir', 'size',
            'mime_type', 'last_modified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ----------------------
# Command
# ----------------------


# ----------------------
# Command
# ----------------------
class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = [
            'id', 'device', 'issued_by', 'command_type', 'payload',
            'status', 'result', 'error_message', 'created_at', 'executed_at', 'finished_at'
        ]
        read_only_fields = [
            'id', 'device', 'status', 'result', 'error_message',
            'created_at', 'executed_at', 'finished_at'
        ]


    



# ----------------------
# FileTransfer
# ----------------------
class FileTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTransfer
        fields = [
            'id', 'device', 'command', 'file_path', 'file_size',
            'status', 'progress', 'created_at', 'finished_at'
        ]
        read_only_fields = ['id', 'created_at', 'finished_at']


# ----------------------
# DeviceConnectionLog
# ----------------------
class DeviceConnectionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConnectionLog
        fields = [
            'id', 'device', 'status', 'ip_address', 'user_agent', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp', 'device']
