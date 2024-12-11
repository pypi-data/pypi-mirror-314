from typing import Optional, Callable, TextIO
from realtime import AsyncRealtimeClient, RealtimeSubscribeStates
import asyncio
import random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PLAYER_LIMIT = 2

class Client:
    def __init__(self, auth: tuple[str, str] | TextIO):
        self.client = None
        self.channel = None
        self.client_thread = None
        self.active = False

        self.user_data = {"username": "", "user_id": None}
    
        project_id, key = None, None
        if isinstance(auth, tuple):
            project_id, key = auth
        else:
            config = {}
            config_lines = auth.readlines()
            for config_line in config_lines:
                key, val = config_line.strip().split('=')
                config[key] = val
            if "PROJECT_ID" not in config or "API_KEY" not in config:
                auth.close()
                raise ValueError(f"No URL or API key provided in `{config}`.")
            
            project_id = config["PROJECT_ID"]
            key = config["API_KEY"]
            auth.close()
    
        self.user_data['user_id'] = self.gen_random_id(length=10)
        project_url = f"wss://{project_id}.supabase.co/realtime/v1"
        self.client = AsyncRealtimeClient(project_url, key)
    
    def __neg__(self):
        self.terminate()
    
    def __del__(self):
        self.terminate()
    
    @staticmethod
    def gen_random_id(length: int = 6):
        return ''.join([random.choice(LETTERS) for _ in range(length)])
    
    @staticmethod
    def _on_subscribe(status: RealtimeSubscribeStates, err: Optional[Exception]):
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            print('Connected!')
        elif status == RealtimeSubscribeStates.CHANNEL_ERROR:
            raise ConnectionError(f'There was an error subscribing to channel: {err.message}')
        elif status == RealtimeSubscribeStates.TIMED_OUT:
            raise ConnectionError('Realtime server did not respond in time.')
        elif status == RealtimeSubscribeStates.CLOSED:
            raise ConnectionError('Realtime channel was unexpectedly closed.')

    def get_username(self):
        return self.user_data["username"]
    
    def set_username(self, usrname: str):
        self.user_data["username"] = usrname
    

    async def create_room(self):
        room_id = self.gen_random_id()
        self.channel = self.client.channel(f"room_{room_id}")
        await self.channel.subscribe(self._on_subscribe)
        self.active = True
        return room_id

    async def join_room(self, room_id: str):
        room_id = f"room_{room_id}"
        self.channel = self.client.channel(room_id)
        await self.channel.subscribe(self._on_subscribe)
        self.active = True

    def add_event_hook(self, event_name: str, func: Callable):
        self.channel.on_broadcast(event_name, func)

    # Use as decorator
    def on_event(self, event_name: str):
        return lambda func: self.add_event_hook(event_name, lambda event: func(event['payload']))

    async def send_event(self, event_name: str, payload):
        print(self.active)
        await self.channel.send_broadcast(event_name, payload)

    async def activate(self):
        await self.client.connect()
        
    async def _listen_blocking(self):
        print("Listening!")
        await self.client.listen()

    def listen(self):
        self.active = True
        self.client_thread = asyncio.create_task(self._listen_blocking())

    def terminate(self):
        if self.client_thread == None:
            raise ValueError("No thread initialized yet.")
        self.client_thread.cancel()
        self.active = False
