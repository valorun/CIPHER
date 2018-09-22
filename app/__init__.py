#!/usr/bin/python
# coding: utf-8

import logging
from os import urandom
from flask import Flask
from flask_socketio import SocketIO
from .model import db
from .constants import SERVER_DATABASE

socketio = SocketIO()

raspies = []

def create_app(debug=False):
    app = Flask(__name__)

    app.debug = debug
    app.secret_key = urandom(12)

    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SERVER_DATABASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
