import asyncio
import json
from typing import Optional

import websockets
from websockets.http import Headers
from threedi_cmd.websockets.settings import WebSocketSettings


class WebsocketClient(object):
    def __init__(self, settings: WebSocketSettings):
        self.settings = settings
        self.websocket = None
        self.do_listen = True
        self.queue = asyncio.Queue()
        self._connected = False

    def get_queue(self):
        return self.queue

    async def is_connected(self):
        while self._connected is False:
            await asyncio.sleep(0.5)

    @property
    def user_agent(self):
        return {
            "user-agent": "simulation-runner"
        }

    async def listen(self, endpoint_uri: str):
        uri = f"{self.settings.proto}://{self.settings.host}/{self.settings.api_version}/{endpoint_uri}"
        headers = Headers(authorization=f"{self.settings.token}")
        headers.update(**self.user_agent)
        sim_time: Optional[int] = None
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            self.websocket = websocket
            self._connected = True
            async for message in websocket:
                try:
                    message = json.loads(message)
                    try:
                        sim_time = message["data"]["time"]
                    except (KeyError, TypeError):
                        pass
                    if sim_time is not None:
                        message["sim_time"] = sim_time
                    await self.queue.put(message)
                except websockets.exceptions.ConnectionClosedOK:
                    self.do_listen = False

    async def close(self):
        self.do_listen = False
        if self.websocket:
            await self.websocket.close()
