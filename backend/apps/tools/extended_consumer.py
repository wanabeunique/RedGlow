from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user
from apps.authentication.models import User
from apps.tools.validators import validate_json
from typing import Awaitable

class ExtendedAsyncConsumer(AsyncJsonWebsocketConsumer):
    group_name_prefix: str | None = None
    user: User | None = None
    acceptable_keys: dict[str,dict[str,type]] | None = None
    
    async def general_connect(self) -> Awaitable:
        self.user: User = await get_user(self.scope)
        if not (self.user and self.user.is_authenticated):
            return self.close
        self.username = self.user.username
        self.group_name = f'{self.group_name_prefix}_{self.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        return self.accept

    async def receive_json(self, data_json: dict, **kwargs) -> Awaitable | None:
        self.user = await get_user(self.scope)
        if not (self.user and self.user.is_authenticated):
            await self.close()
            return
        
        message_type = data_json.pop('type', None)

        if message_type is None:
            await self.send_status_info('Invalid type', error=True)
            return

        if message_type not in self.acceptable_keys.keys():
            await self.send_status_info('Invalid type', error=True)
            return

        is_json_valid = await validate_json(data_json, self.acceptable_keys.get(message_type))

        if not is_json_valid:
            await self.send_status_info('Invalid data', error=True)
            return

        method = getattr(self, message_type, None)

        return method

    async def send_status_info(self, message, error=False):
        await self.send_json(
            {
                'status': 'error' if error else 'success',
                'message': message
            }
        )

    async def discard_group(self):
        if hasattr(self,"group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)