#!/usr/bin/python
# coding: utf-8

from flask import Flask
from flask_socketio import SocketIO
from chatterbot import ChatBot
from .model import db
from .constants import *
import app.chatbot

chatbot = ChatBot(
    'Hector',
    #trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        #{
        #    'import_path': 'chatterbot.logic.MathematicalEvaluation',
        #    'language': 'FRE'
        #},
        {
            'import_path': "app.chatbot.entity_adapter.EntityAdapter"
        }
    ],
    database=CHATBOT_DATABASE
)

#chatbot.train(
#    os.path.join(os.path.dirname(__file__),'chatbot/corpus_test.yml')
#)

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)

    app.debug = debug
    app.secret_key = os.urandom(12)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SERVER_DATABASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
