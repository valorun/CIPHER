#!/usr/bin/python
# coding: utf-8

from os import urandom
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from .model import db
from .constants import SERVER_DATABASE, LOG_FILE, MQTT_BROKER_URL, MQTT_BROKER_PORT

socketio = SocketIO() # socketio server used to communicate with web client
mqtt = Mqtt() # mqtt client, need to be connected to a brocker (in local)

raspies = []

def create_app(debug=False):
    app = Flask(__name__)

    app.debug = debug
    app.secret_key = urandom(12)

    app.config['SQLALCHEMY_DATABASE_URI'] = SERVER_DATABASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MQTT_BROKER_URL'] = MQTT_BROKER_URL
    app.config['MQTT_BROKER_PORT'] = MQTT_BROKER_PORT
    app.config['MQTT_KEEPALIVE'] = 5
    db.app = app
    db.init_app(app)
    db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    mqtt.init_app(app)
    mqtt.subscribe("server/raspi_connect")
    mqtt.subscribe("server/raspi_disconnect")
    
    return app

def create_logger(debug=False):
    if debug:
        debug_level = logging.DEBUG
    else:
        debug_level = logging.ERROR
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000)
    formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
    file_handler.setFormatter(formatter)
    root_logger=logging.getLogger()
    logging.getLogger('engineio').propagate = False # hide engineio logs to avoid flood
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.setLevel(debug_level)
    return root_logger