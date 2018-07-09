#!/usr/bin/python
# coding: utf-8

import os
import logging
from flask import request
from flask_socketio import SocketIO, emit
import json
from .. import socketio, chatbot, KEYWORDS_DATASET
from app.model import  Sequence, Relay, Button


@socketio.on('client_connect', namespace='/client')
def client_connect():
	logging.info("Client "+str(request.remote_addr)+' connected.')

@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    logging.info('Client '+ str(request.remote_addr) +' disconnected')
    emit("stop", namespace="/servo", broadcast=True)


@socketio.on('train', namespace='/client')
def train_chatbot(conversation):
    logging.info("Chatbot trained with: ".join(conversation))
    chatbot.train(conversation)


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
        emit("update_state", pin, namespace="/relay", broadcast=True)

#Met a jour l'etat des relais cote client à la demande d'un raspberry
@socketio.on('update_state_for_client', namespace='/relay')
def update_state_for_client(pin, state):
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
