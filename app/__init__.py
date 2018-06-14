#!/usr/bin/python
# coding: utf-8

from flask import Flask
from flask_socketio import SocketIO
from .model import db
import os

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)

    app.debug = debug
    app.secret_key = os.urandom(12)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'server_data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
