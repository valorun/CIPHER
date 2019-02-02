#!/usr/bin/python
# coding: utf-8

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .chatbot.chatbot import ChatBotWrapper
from .constants import CONFIG_FILE, CHATBOT_DATABASE
import os
import json

db = SQLAlchemy()

class Sequence(db.Model):
	id = db.Column(db.String(50), primary_key=True)
	value = db.Column(db.Text, nullable=False)
	enabled = db.Column(db.Boolean, nullable=False)

	def __repr__(self):
		return '<Sequence %r>' % self.id

class Relay(db.Model):
	label = db.Column(db.String(50), primary_key=True)
	pin = db.Column(db.String(4), nullable=False)
	enabled = db.Column(db.Boolean, nullable=False)
	parity = db.Column(db.String(20), nullable=False)
	raspi_id = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return '<Relay %r : >' % self.label

class ConfigFile():
	def saveOption(self, key: str, data):
		"""
		Save an option into the config file.
		"""
		try:
			with open(CONFIG_FILE, 'r') as f:
				content = json.load(f)
		except IOError: #si aucun fichier n'existe, ou si la donnée lue n'est pas en json
			with open(CONFIG_FILE, 'w') as f:
				f.write("") #on créer un nouveau 
			content = {}
		except ValueError:
			content = {}
		content[key] = data
		with open(CONFIG_FILE, 'w') as f:
			json.dump(content, f)

	def loadOption(self, key: str):
		"""
		Load an option from the config file.
		"""
		try:
			with open(CONFIG_FILE, 'r') as f:
				content = json.load(f)
				option = content[key]
		except (IOError):
			with open(CONFIG_FILE, 'w') as f:
				f.write("")
			option = None
		except (KeyError, ValueError):
			option = None
		return option

	# CAMERA URL
	def setCameraUrl(self, url: str):
		self.saveOption("camera_url", url)

	def getCameraUrl(self) -> str:
		return self.loadOption("camera_url")

	# KEYWORD DATASET
	def setKeywordDataset(self, dataset: {}):
		self.saveOption("keyword_dataset", dataset)

	def getKeywordDataset(self) -> {}:
		return self.loadOption("keyword_dataset")

	# COMMANDS GRID
	def setCommandsGrid(self, grid: {}):
		self.saveOption("commands_grid", grid)

	def getCommandsGrid(self) -> {}:
		return self.loadOption("commands_grid")
	
	# WHEELS MODE
	def setWheelsMode(self, mode: bool):
		self.saveOption("wheels_mode", mode)

	def getWheelsMode(self) -> bool:
		mode = self.loadOption("wheels_mode")
		if mode == None:
			mode = False # default mode is for caterpillars
		return mode

	# AUDIO SOURCE
	def setAudioOnServer(self, mode: bool):
		self.saveOption("audio_on_server", mode)

	def getAudioOnServer(self) -> bool:
		mode = self.loadOption("audio_on_server")
		if mode == None:
			mode = False
		return mode

	# CHATBOT LEARNING MODE
	def setChatbotReadOnlyMode(self, mode: bool):
		self.saveOption("chatbot_read_only_mode", mode)

	def getChatbotReadOnlyMode(self) -> bool:
		mode = self.loadOption("chatbot_read_only_mode")
		if mode == None:
			mode = False
		return mode

	# MOTION RASPI ID
	def setMotionRaspiId(self, raspi_id: str):
		self.saveOption("motion_raspi_id", raspi_id)

	def getMotionRaspiId(self) -> str:
		return self.loadOption("motion_raspi_id")
	
	# SERVO RASPI ID
	def setServoRaspiId(self, raspi_id: str):
		self.saveOption("servo_raspi_id", raspi_id)

	def getServoRaspiId(self) -> str:
		return self.loadOption("servo_raspi_id")

config = ConfigFile()

chatbot = ChatBotWrapper(CHATBOT_DATABASE)
chatbot.instantiateChatBot(config.getChatbotReadOnlyMode())