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
from .model import config, db, User

socketio = SocketIO(logger=True)  # socketio server used to communicate with web client
mqtt = Mqtt()  # mqtt client, need to be connected to a brocker (in local)


def create_app(debug=False):
    app = Flask(__name__)

    app.debug = False  # weid behavior, create two instances of flask
    app.secret_key = urandom(12)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_file()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MQTT_BROKER_URL'] = config.get_mqtt_broker_url()
    app.config['MQTT_BROKER_PORT'] = config.get_mqtt_broker_port()
    app.config['MQTT_KEEPALIVE'] = 5

    from .core import core as core_blueprint
    from .security import security as security_blueprint

    app.register_blueprint(core_blueprint)
    app.register_blueprint(security_blueprint)

    loaded_plugins = []
    # load all specified plugins
    for p_name in config.get_plugins():
        try:
            # find the plugin object ...
            module = importlib.import_module('.plugins.' + p_name, package='cipher')
            p = getattr(module, p_name)
            loaded_plugins.append(p)
            # then register its blueprint
            p.register(app, loaded_plugins)
        except Exception as e:
            logging.error("Failed to load plugin '" + p_name + "': {0}".format(e))
            exit(1)

    db.app = app
    db.init_app(app)
    db.create_all()

    # create admin if not exists
    exists = User.query.filter_by(username='admin').first()
    if not exists:
        new_db_user = User(username='admin', password='cGFzc3dvcmQ=', active=True)
        db.session.merge(new_db_user)
        db.session.commit()

    socketio.init_app(app)
    mqtt.init_app(app)
    mqtt.subscribe('server/#')
    mqtt.subscribe('hermes/intent/#')

    return app


class SocketIOHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        socketio.emit('logging', msg, namespace='/client')


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
                'filename': config.get_log_file(),
                'maxBytes': 1024
            },
            'socketio': {
                'formatter': 'default',
                'class': 'cipher.SocketIOHandler',
            }
        },
        'root': {
            'level': log_level,
            'handlers': ['default', 'file', 'socketio'],
            'formatter': 'default'
        },
        'loggers': {
            'socketio.server': {'handlers': ['default', 'file'], 'propagate': False},
            'flask.flask_mqtt': {'handlers': ['default', 'file', 'socketio']},
            'sqlalchemy': {'handlers': ['default', 'file', 'socketio']},
        }
    })
