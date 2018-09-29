#!/usr/bin/python
# coding: utf-8

from os import urandom
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_socketio import SocketIO
from .model import db
from .constants import SERVER_DATABASE, LOG_FILE

socketio = SocketIO()

raspies = []

def create_app(debug=False):
    app = Flask(__name__)

    app.debug = debug
    app.secret_key = urandom(12)

    app.config['SQLALCHEMY_DATABASE_URI'] = SERVER_DATABASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

def create_logger():
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000)
    formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
    file_handler.setFormatter(formatter)
    root_logger=logging.getLogger()
    logging.getLogger('engineio').propagate = False # hide engineio logs to avoid flood
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)
    return root_logger