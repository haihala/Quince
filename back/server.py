import os
import asyncio
import websockets
import json
import pprint
import time
import ssl
import pathlib

class Server:
    def __init__(self):
        self.debug = False
        self.port = os.getenv('QUINCE_PORT', '5000')
        self.host = os.getenv('QUINCE_HOST', '0.0.0.0')
        self.datadir = os.getenv('QUINCE_DATA', 'data')
        if not os.path.isabs(self.datadir):
            self.datadir = os.path.join(os.getcwd(), self.datadir)
        
        assert not os.path.isfile(self.datadir), "A file exists where the data directory is supposed to go"
        # Directory doesn't exist. Make one.
        if not os.path.isdir(self.datadir):
            os.mkdir(self.datadir)
        
        # Intentionally don't initiate this. Don't crawl the datadir.
        self.notes = {}     # Key is node id and filename, value is a list of sockets connected to it.
        self.locks = set()

    async def lockRead(self, note):
        # Wait for file to be unlocked, lock, read file, unlock
        path = os.path.join(self.datadir, note)
        while note in self.locks:
            # Don't do anything if file is locked.
            await asyncio.sleep(0.1)
        self.locks.add(note)            
        with open(path) as f:
            content = f.read() 
        self.locks.remove(note)
        return content

    async def lockWrite(self, note, content):
        # Wait for file to be unlocked, lock, write to file, unlock
        path = os.path.join(self.datadir, note)
        while note in self.locks:
            # Don't do anything if file is locked.
            await asyncio.sleep(0.1)
        self.locks.add(note)
        with open(path, 'w') as f:
            f.write(content)
        self.locks.remove(note)

    async def lockDelete(self, note):
        # Wait for file to be unlocked, lock, delete file, unlock
        path = os.path.join(self.datadir, note)
        while note in self.locks:
            # Don't do anything if file is locked.
            await asyncio.sleep(0.1)
        self.locks.add(note)
        os.remove(path)
        self.locks.remove(note)

    async def lockTouch(self, note):
        # Wait for file to be unlocked, lock, touch file, unlock
        path = os.path.join(self.datadir, note)
        while note in self.locks:
            # Don't do anything if file is locked.
            await asyncio.sleep(0.1)
        self.locks.add(note)
        pathlib.Path(path).touch()
        self.locks.remove(note)


    def inverseNotes(self):
        # God I love python
        return {sock: note for note, socks in self.notes.items() for sock in socks}

    async def backgroundChugger(self):
        # For the background thread. Responsible for:
        # Deleting closed notes that haven't been edited in a while.
        # Update catalogue of existing notes
        while self.server.sockets:
            deleted = set()

            for note, socks in self.notes.items():
                path = os.path.join(self.datadir, note)
                assert os.path.isfile(path), "About to check a note that doesn't exist"
                if not socks and os.path.getmtime(path) + 60 < time.time():
                    # File has no active sockets and hasn't been modified for a minute
                    await self.lockDelete(note)
                    deleted.add(note)
            
            for note in deleted:
                del self.notes[note]
            
            for sock, note in self.inverseNotes().items():
                if sock not in self.server.websockets:
                    self.notes[note].remove(sock)
                    await self.lockTouch(note)

            await asyncio.sleep(1)

    async def start(self, loop):
        print("Starting server")
        ssl_context = ssl.create_default_context()
        #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        #fullchain_pem = pathlib.Path("/etc/letsencrypt/live/whiteboard.tunk.org/fullchain.pem")
        #privkey_pem = pathlib.Path("/etc/letsencrypt/live/whiteboard.tunk.org/privkey.pem")
        #ssl_context.load_cert_chain(fullchain_pem, keyfile=privkey_pem)
        self.server = await websockets.serve(self.handler, self.host, self.port, ssl=ssl_context)
        loop.create_task(self.backgroundChugger())
        return self.server

    async def fetch(self, sock, noteId):
        # Returns the contents of the note
        if noteId in self.notes:
            # Note exists and can be read.
            content = await self.lockRead(noteId)

            if sock not in self.notes[noteId]:
                # New user, old note
                self.notes[noteId].add(sock)
        else:
            # New user new note
            content = ""
            self.notes[noteId] = {sock}

        # Either make a blank file or refresh it so the system knows not to delete it.
        await self.lockTouch(noteId)

        return {"content": content, "result": "ok"}

    async def update(self, sock, noteId, data):
        # User updated a note
        # Loop through other readers of that note and send them the update.
        if noteId in self.notes:
            # Change file
            # Straight up raw dog it. If they send you 15 terabytes of kiddie porn so be it.
            await self.lockWrite(noteId, data)

            # Send updates to others
            refresh = await self.fetch(sock, noteId)
            for s in self.notes[noteId]:
                if s != sock:
                    s.send(refresh)
                
            return {"result": "ok"}
        else:
            # Mitäs vittua
            return {"result": "fail", "error": "Writing to a note that doesn't exist."}


    async def handler(self, websocket, path):
        async for message in websocket:
            response = ""
            try:
                data = json.loads(message)
        
                if self.debug:
                    print('server received: ', end='')
                    pprint.pprint(data)
                
                if "type" not in data:
                    response = {"result": "fail", "error": "Missing type parameter"}
                elif data["type"] == "fetch":
                    response = await self.fetch(websocket, data["id"])
                elif data["type"] == "update":
                    response = await self.update(websocket, data["id"], data["content"])
                else:
                    response = {"result": "fail", "error": "Invalid type"}
            except:
                # Reply with error
                response = {"result": "fail", "error": "Couldn't parse json from data"}
        
            await websocket.send(json.dumps(response))
