from flask import Flask
from flask_socketio import SocketIO

#app = Flask("Quince", static_folder='front/build', static_url_path='/')
app = Flask("Quince")
socketio = SocketIO(app)

@app.route("/flask")
def index():
    return "Hello World"

@socketio.on("event", namespace="/<note>/")
def process_note(note):
    print("Got an event on note '{}'".format(note))
