import os
import asyncio
import websockets

class Server:
    def __init__(self):
        self.datadir = os.getenv('QUINCE_DATA', 'data')
        if not os.path.isabs(self.datadir):
            self.datadir = os.path.join(os.getcwd(), self.datadir)
        
        assert not os.path.isfile(self.datadir), "A file exists where the data directory is supposed to go"
        if not os.path.isdir(self.datadir):
            os.mkdir(self.datadir)

    def get_port(self):
        return os.getenv('QUINCE_PORT', '5000')

    def get_host(self):
        return os.getenv('QUINCE_HOST', 'localhost')

    def start(self):
        print("Starting server")
        return websockets.serve(self.handler, self.get_host(), self.get_port())

    async def handler(self, websocket, path):
      async for message in websocket:
        print('server received: {}'.format(message))
        await websocket.send(message)