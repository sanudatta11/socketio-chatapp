from flask import Flask, render_template
from flask_socketio import SocketIO

from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

socketio = SocketIO(app)

from app import views