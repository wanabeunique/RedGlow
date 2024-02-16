from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user
from apps.authentication.models import User
from apps.tools.validators import validate_json

class ExtendedAsyncConsumer(AsyncJsonWebsocketConsumer):
    group_name_prefix: str | None = None
    user: User | None = None
    acceptable_keys: dict[str,dict[str,type]] | None = None
    
    async def connect(self):
        user: User = await get_user(self.scope)
        if not (user and user.is_authenticated):
            await self.close()
            return
        self.username = user.username
        self.group_name = f'{self.group_name_prefix}_{self.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive_json(self, data_json: dict, **kwargs):
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

        method = getattr(self, message_type)

        await method(data_json)

    async def send_status_info(self, message, error=False):
        await self.send_json(
            {
                'status': 'error' if error else 'success',
                'message': message
            }
        )