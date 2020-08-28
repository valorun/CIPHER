# coding: utf-8

import eventlet
eventlet.monkey_patch()

from os import urandom
import logging
import importlib
from collections import deque
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from .config import core_config
from .model import db, User

socketio = SocketIO(logger=True, async_mode='eventlet')  # socketio server used to communicate with web client
mqtt = Mqtt()  # mqtt client, need to be connected to a brocker (in local)


def create_app(debug=False):
    app = Flask(__name__)

    app.debug = False  # weird behavior, create two instances of flask
    app.secret_key = urandom(12)

    app.config['SQLALCHEMY_DATABASE_URI'] = core_config.DATABASE_FILE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MQTT_BROKER_URL'] = core_config.MQTT_BROKER_URL
    app.config['MQTT_BROKER_PORT'] = core_config.MQTT_BROKER_PORT
    app.config['MQTT_KEEPALIVE'] = 5

    from .core import core as core_blueprint
    from .security import security as security_blueprint

    app.register_blueprint(core_blueprint)
    app.register_blueprint(security_blueprint)

    loaded_plugins = []
    # load all specified plugins
    for p_name in core_config.PLUGINS:
        try:
            # find the plugin object ...
            module = importlib.import_module('.plugins.' + p_name, package='cipher')
            p = getattr(module, p_name)
            loaded_plugins.append(p)
            # then register its blueprint
            p.register(app, loaded_plugins)
            logging.info("✓ - Plugin '" + p_name + "' loaded")
        except Exception as e:
            logging.error("❌ - Failed to load plugin '" + p_name + "': {0}".format(e))
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
    
    @mqtt.on_connect()
    def on_server_connect(client, userdata, flags, rc):
        """
        Function called when the server connects to the broker.
        """
        mqtt.subscribe('server/#')
        mqtt.subscribe('client/connect')
        mqtt.publish('server/connect')
        logging.info("Connected to broker.")
        for p in loaded_plugins:
            for f in p.startup_functions:
                f()

    socketio.init_app(app)
    mqtt.init_app(app)

    return app


class SocketIOHandler(logging.Handler):
    log_queue = deque(maxlen=30)

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        if socketio is not None and socketio.server is not None:
            socketio.emit('logging', msg, namespace='/client')
        SocketIOHandler.log_queue.append(self.format(record))


def setup_logger(debug=False):
    if debug:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s %(levelname)-8s [%(name)s] %(message)s',
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
                'filename': core_config.LOG_FILE,
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
            #'socketio.server': {'handlers': ['default', 'file'], 'propagate': False},
            'flask.flask_mqtt': {'handlers': ['default', 'file', 'socketio']},
            'sqlalchemy': {'handlers': ['default', 'file', 'socketio']},
        }
    })
