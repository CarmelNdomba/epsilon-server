import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models.device import Device, DeviceConnectionLog
from channels.db import database_sync_to_async


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accepter la connexion
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to server"}))

    async def receive(self, text_data=None, bytes_data=None):
        # On attend un JSON avec device_uid et info
        data = json.loads(text_data)
        device_uid = data.get("device_uid")
        info = data.get("info", {})

        # Vérifier si le device existe, sinon créer
        device, created = Device.objects.get_or_create(device_uid=device_uid)
        device.name = info.get("name")
        device.manufacturer = info.get("manufacturer")
        device.model = info.get("model")
        device.android_version = info.get("android_version")
        device.is_online = True
        await database_sync_to_async(device.save)()

        # Log de connexion
        log = DeviceConnectionLog(device=device, status="connected")
        await database_sync_to_async(log.save)()

        # Confirmer au device
        await self.send(text_data=json.dumps({"status": "ok", "device_id": str(device.id)}))

    async def disconnect(self, close_code):
        # Ici on pourrait récupérer device_uid pour mettre is_online=False
        pass
