from flask import Flask
from flask_socketio import SocketIO

app = Flask("Quince", static_folder='front/build', static_url_path='/')
socketio = SocketIO(app)

@app.route("/")
def index():
    return app.send_static_file('index.html')

@socketio.on("event", namespace="/<note>/")
def process_note(note):
    print("Got an event on note '{}'".format(note))