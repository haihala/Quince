from flask import Flask
app = Flask("Quince", static_folder='front/build', static_url_path='/')

@app.route("/")
def index():
    return app.send_static_file('index.html')

