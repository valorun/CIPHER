#!/usr/bin/python
# coding: utf-8

from flask import Flask
from flask_socketio import SocketIO
from .model import db
from chatterbot import ChatBot
import os

KEYWORDS_DATASET=os.path.join(os.path.dirname(__file__),"keywords_dataset.json")
CHATBOT_DATABASE=os.path.join(os.path.dirname(__file__),"chatbot.db")
SCRIPTS_LOCATION=os.path.join(os.path.dirname(__file__),"scripts/")
SOUNDS_LOCATION=os.path.join(os.path.dirname(__file__),"sounds/")

chatbot = ChatBot(
    'Hector',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            'import_path': "chatterbot.logic.MathematicalEvaluation",
            'language': "FRE"
        },
        {
            'import_path': "chatterbot.logic.BestMatch"
        }
    ],
    database=CHATBOT_DATABASE
)
#chatbot.train(
#    './corpus_test.yml'
#)

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
