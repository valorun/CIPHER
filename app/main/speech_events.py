#!/usr/bin/python
# coding: utf-8

import logging
from flask_socketio import SocketIO, emit
from app.model import config, chatbot
import json
from .. import socketio

#Sauvegarde l'entrainement à la reconnaissance de mots clés
@socketio.on('save_keywords_dataset', namespace='/client')
def save_keywords_dataset(dataset):
	logging.info("Saving keywords dataset")
	config.setKeywordDataset(json.loads(dataset))

#Charge l'entrainement à la reconnaissance de mots clés
@socketio.on('load_keywords_dataset', namespace='/client')
def load_keywords_dataset():
	dataset = config.getKeywordDataset()
	if dataset == None:
		dataset = []
	emit("load_keywords_dataset", dataset, namespace="/client", broadcast=True)

@socketio.on('train', namespace='/client')
def train_chatbot(conversation):
	print(conversation)
	logging.info("Chatbot trained with: ".join(conversation))
	chatbot.train(conversation)