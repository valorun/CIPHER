#!/usr/bin/python
# coding: utf-8

import logging
from flask_socketio import SocketIO, emit
from app.model import config, chatbot
import json
from .. import socketio

@socketio.on('save_keywords_dataset', namespace='/client')
def save_keywords_dataset(dataset):
	"""
	Save the training to keyword recognition.
	"""
	logging.info("Saving keywords dataset")
	config.setKeywordDataset(json.loads(dataset))

@socketio.on('load_keywords_dataset', namespace='/client')
def load_keywords_dataset():
	"""
	Load the training to keyword recognition.
	"""
	dataset = config.getKeywordDataset()
	if dataset == None:
		dataset = []
	emit("load_keywords_dataset", dataset, namespace="/client", broadcast=True)

@socketio.on('train', namespace='/client')
def train_chatbot(conversation):
	logging.info("Chatbot trained with: ".join(conversation))
	chatbot.train(conversation)