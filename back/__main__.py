from server import Server

import asyncio

if __name__ == "__main__":
    ws = Server()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws.start(loop))
    loop.run_forever() 