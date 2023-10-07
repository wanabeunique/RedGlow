from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user, logout
import json

class FriendConsumer(AsyncJsonWebsocketConsumer):
    groups = ['friends']
    async def connect(self):
        user = await get_user(self.scope)
        self.username = user.username
        self.group_name = f'friends_{self.username}'
        if not user.is_anonymous:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    # async def receive(self, text_data):

    #     user = await get_user(self.scope)

    #     dataJson = json.loads(text_data)

    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         text_data=json.dumps({'type':'friend.invite',"invite": dataJson['invite']})
    #     )

        
    async def friend_invite(self,event):
        user = await get_user(self.scope)
        if not user.is_anonymous:
            invite = event.get('invite',None)
            if not invite:
                raise ValueError(f'Сообщение не может быть пустым')

            await self.send(text_data=json.dumps({"invite": invite}))
        else:
            await self.close()