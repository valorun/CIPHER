#!/usr/bin/python
# coding: utf-8

import eventlet
eventlet.monkey_patch(socket=False)

from os import urandom
import logging
import importlib
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from .model import db
from .constants import SERVER_DATABASE, LOG_FILE, MQTT_BROKER_URL, MQTT_BROKER_PORT, PLUGINS

socketio = SocketIO(logger=True)  # socketio server used to communicate with web client
mqtt = Mqtt()  # mqtt client, need to be connected to a brocker (in local)


def create_app(debug=False):
    app = Flask(__name__)

    app.debug = False  # weid behavior, create two instances of flask
    app.secret_key = urandom(12)

    app.config['SQLALCHEMY_DATABASE_URI'] = SERVER_DATABASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MQTT_BROKER_URL'] = MQTT_BROKER_URL
    app.config['MQTT_BROKER_PORT'] = MQTT_BROKER_PORT
    app.config['MQTT_KEEPALIVE'] = 5

    from .core import core as core_blueprint
    from .security import security as security_blueprint

    app.register_blueprint(core_blueprint)
    app.register_blueprint(security_blueprint)

    loadedPlugins = []
    # load all specified plugins
    for pPame in PLUGINS:
        try:
            # find the plugin object ...
            module = importlib.import_module('.plugins.' + pPame, package='cipher')
            p = getattr(module, pPame)
            loadedPlugins.append(p)
            # then register its blueprint
            p.register(app, loadedPlugins)
        except Exception as e:
            logging.error("Failed to load plugin '" + pPame + "': {0}".format(e))
            exit(1)

    db.app = app
    db.init_app(app)
    db.create_all()

    socketio.init_app(app)
    mqtt.init_app(app)
    mqtt.subscribe('server/#')
    mqtt.subscribe('hermes/intent/#')

    return app


def setup_logger(debug=False):
    if debug:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(name)s: %(message)s',
        }},
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'file': {
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_FILE,
                'maxBytes': 1024
            }
        },

        'root': {
            'level': log_level,
            'handlers': ['default', 'file']
        },
        'loggers': {
            'socketio': {},
            'flask.flask_mqtt': {},
            'sqlalchemy': {},
        }
    })
