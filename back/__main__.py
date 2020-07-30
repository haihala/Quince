from server import Server

import asyncio

if __name__ == "__main__":
    ws = Server()
    asyncio.get_event_loop().run_until_complete(ws.start())
    asyncio.get_event_loop().run_forever() 