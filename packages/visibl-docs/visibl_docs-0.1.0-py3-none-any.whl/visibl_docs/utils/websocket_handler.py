import asyncio
import websockets
import json
from typing import Set, Dict

class WebSocketHandler:
    def __init__(self):
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        self.is_running = False
        self.view_types: Dict[websockets.WebSocketServerProtocol, str] = {}

    async def register(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data.get('type') == 'register':
                    self.view_types[websocket] = data.get('viewType')
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            self.view_types.pop(websocket, None)

    async def start_server(self):
        if not self.is_running:
            self.server = await websockets.serve(
                self.register,
                'localhost',
                3000,
                path='/ws/client'
            )
            self.is_running = True
            print("WebSocket server started on ws://localhost:3000/ws/client")

    async def broadcast_update(self, content: str, code_blocks: list = None):
        if not self.clients:
            print("No clients connected - updates will be missed")
            return

        for client in self.clients:
            view_type = self.view_types.get(client)
            if not view_type:
                continue

            try:
                if view_type == 'code' and code_blocks:
                    await client.send(json.dumps({
                        'viewType': 'code',
                        'data': {'blocks': code_blocks}
                    }))
                elif view_type == 'metrics':
                    await client.send(json.dumps({
                        'viewType': 'metrics',
                        'data': {'value': len(code_blocks) if code_blocks else 0}
                    }))
            except websockets.exceptions.ConnectionClosed:
                continue

_ws_handler = None

def get_websocket_handler():
    global _ws_handler
    if _ws_handler is None:
        _ws_handler = WebSocketHandler()
    return _ws_handler