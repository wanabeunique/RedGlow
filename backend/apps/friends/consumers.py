from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user, logout
import json

class FriendConsumer(AsyncJsonWebsocketConsumer):
    groups = ['friends']
    async def connect(self):
        user = await get_user(self.scope)
        if user and user.is_authenticated:
            self.username = user.username
            self.group_name = f'friends_{self.username}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data):

        user = await get_user(self.scope)
        if user and user.is_authenticated:
            dataJson = json.loads(text_data)
            messageType = dataJson.get('type')
            if messageType:
                target = dataJson.get("target")
                await self.channel_layer.group_send(
                    f'friends_{target}',
                    {'type':f'friend.{messageType}',"target": user.username}
                )
        else:
            await self.close()
    async def friend_accept(self,event):
        await self.send(text_data=json.dumps({"type": 'accept','target': event.get('target')}))

        
    async def friend_invite(self,event):
        await self.send(text_data=json.dumps({"type": 'invite','target': event.get('target')}))