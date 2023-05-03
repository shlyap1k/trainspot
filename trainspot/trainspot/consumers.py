import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('aboba connect')
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print('aboba recieve')
        data = json.loads(text_data)
        await self.send_signal(data)

    async def send_signal(self, data):
        print('aboba send')
        await self.send(json.dumps(data))