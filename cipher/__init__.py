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
from .constants import SERVER_DATABASE, LOG_FILE, MQTT_BROKER_URL, MQTT_BROKER_PORT

socketio = SocketIO(logger=True) # socketio server used to communicate with web client
mqtt = Mqtt() # mqtt client, need to be connected to a brocker (in local)

plugins = [ 'dashboard', 'commands', 'speech', 'editor', 'debug', 'sequences', 'settings' ] # all the different  page available in the navbar

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

    from .core import core as core_blueprint
    from .security import security as security_blueprint

    app.register_blueprint(core_blueprint)
    app.register_blueprint(security_blueprint)

    loaded_plugins = []
    # load all specified plugins
    for p_name in plugins:
        try:
            # find the plugin object ...
            module = importlib.import_module('.plugins.' + p_name, package='cipher')
            p = getattr(module, p_name)
            loaded_plugins.append(p)
            # then register its blueprint
            p.register(app, loaded_plugins)
        except Exception:
            logging.error('Failed to load plugin \'' + p_name + '\'')
            exit(1)

    socketio.init_app(app)
    #mqtt.init_app(app)
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
            'format': '%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s',
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
            'flask': {},
            'sqlalchemy': {},
        }
    })
