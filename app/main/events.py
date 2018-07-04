#!/usr/bin/python
# coding: utf-8

import os
import logging
from flask import request, current_app
from flask_socketio import SocketIO, emit
from chatterbot import ChatBot
import json
from .. import socketio
from .sequence_reader import SequenceReader
from app.model import  Sequence, Relay, Button

sequence_reader = SequenceReader()

KEYWORDS_DATASET="keywords_dataset.json"

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
    database="./chatbot.db"
)
#chatbot.train(
#    './corpus_test.yml'
#)

@socketio.on('client_connect', namespace='/client')
def client_connect():
	logging.info("Client "+str(request.remote_addr)+' connected.')

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    logging.info('Client '+ str(request.remote_addr) +' disconnected')

@socketio.on('speech_detected', namespace='/client')
def speech_detected(transcript):
    logging.info("Received data: " + transcript)
    response = str(chatbot.get_response(transcript))
    if(len(response.split("]"))>1):
        seq_name=response.split("[")[1].split("]")[0]
        seq = Sequence.query.filter_by(id=seq_name).first()
        response = response.split("]")[1]
        #Si une séquence existe et est activée, on la lance
        if(seq!=None and seq.enabled):
            seq_data = seq.value
            logging.info('Command received: '+seq_name)
            sequence_reader.readSequence(json.loads(seq_data))
    emit("response", response)

@socketio.on('train', namespace='/client')
def train_chatbot(conversation):
    logging.info("Chatbot trained with: ".join(conversation))
    chatbot.train(conversation)

@socketio.on('play_sequence', namespace='/client')
def play_sequence(seq_name):
    seq = Sequence.query.filter_by(id=seq_name).first()
    if(seq!=None and seq.enabled):
        seq_data = seq.value
        logging.info('Executing sequence '+seq_name)
        sequence_reader.readSequence(current_app._get_current_object(), json.loads(seq_data))

@socketio.on('command', namespace='/client')
def command(label):
    logging.info("Received command: "+label)
    sequence_reader.executeAction(current_app._get_current_object(), label);



@socketio.on('shutdown', namespace='/client')
def shutdown():
    logging.info("Shutdown rasperries")
    emit("shutdown", namespace="/raspi", broadcast=True)
    #os.system('shutdown -h now')

@socketio.on('reboot', namespace='/client')
def reboot():
    logging.info("Reboot rasperries")
    emit("reboot", namespace="/raspi", broadcast=True)
    #os.system('reboot -h now')


#Met a jour l'etat des relais cote client à la demande d'un client
@socketio.on('update_relays_state', namespace='/client')
def update_relays_state():
    logging.info("Updating relay status on client")
    for relay in Relay.query.distinct(Relay.pin):
        pin=relay.pin
        emit("get_state", pin, namespace="/relay", broadcast=True)

#Met a jour l'etat des relais cote client à la demande d'un raspberry
@socketio.on('update_state', namespace='/relay')
def update_state(pin, state):
    logging.info("Updating relay status on client")
    for relay in Relay.query.filter_by(pin=pin):
        label=relay.label
        emit("update_relay_state", {'label':label, 'state':state}, namespace="/client", broadcast=True)


#Sauvegarde l'entrainement à la reconnaissance de mots clés
@socketio.on('save_keywords_dataset', namespace='/client')
def save_keywords_dataset(dataset):
    logging.info("Saving keywords dataset")
    with open(KEYWORDS_DATASET, 'w') as file:
        file.write(dataset)

#Sauvegarde l'entrainement à la reconnaissance de mots clés
@socketio.on('load_keywords_dataset', namespace='/client')
def load_keywords_dataset():
    with open(KEYWORDS_DATASET) as f:
        dataset = json.load(f)
        emit("load_keywords_dataset", dataset, namespace="/client", broadcast=True)
