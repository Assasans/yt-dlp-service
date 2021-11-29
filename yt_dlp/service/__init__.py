import datetime
import json
import asyncio
import math

import websockets

from yt_dlp.utils import DownloadError

class WebSocketService:
    def __init__(self, url):
        self.url = url
        self.client = None

    async def handle(self, message):
        from yt_dlp import _real_main

        try:
            # print(f'[websocket] Handling message: {message}')

            packet = json.loads(message)
            action = packet['action']
            nonce = packet['nonce']

            # print(f'[websocket] Packet: {packet}')
            # print(f'[websocket] Action: {action}, nonce: {nonce}')

            if action == 1:
                data = packet['data']
                command = data['command']

                print(f'[websocket] Action: {action}, nonce: {nonce}, command: {command}')

                _real_main(self.client, nonce, command)
                # print(f'[websocket] Execution completed')

                completedPacket = {
                    'nonce': nonce,
                    'action': 3,
                    'data': {}
                }
                serialized = json.dumps(completedPacket)

                # await asyncio.sleep(0.1)
                # await self.client.send(serialized)
                # print(f'Sent: [nonce: {nonce}, action: 3, data: [] ]')
                # print(f'Sent {serialized}...')
        except DownloadError as e:
            print(f'Download error: {e}')

    async def run(self):
        # protocol = 'wss' if self.secure else 'ws'
        async with websockets.connect(self.url) as self.client:
            print(f'Connected to WebSocket server')

            # Identify as yt-dlp client
            completedPacket = {
                'nonce': math.floor(datetime.datetime.today().timestamp() * 1000),
                'action': 4,
                'data': {
                    'type': 1
                }
            }
            serialized = json.dumps(completedPacket)

            await self.client.send(serialized)
            print(f'Identified as yt-dlp client')

            async for message in self.client:
                await self.handle(message)
