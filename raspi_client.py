#!/usr/bin/python
# coding: utf-8

import time
from enum import Enum
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
import logging

class ActionType(Enum): # différents types d'actions pris en charge par les rasperries
	MOTION=1
	SERVO=2
	RELAY=3

CLIENT_MODES=[ActionType.MOTION, ActionType.SERVO, ActionType.SPEECH]

class MotionNamespace(BaseNamespace):
	def on_command(self, *args):
		print('motion', args)

	def on_command(self, *args):
		print('motion111', args)

class ServoNamespace(BaseNamespace):
	def on_command(self, *args):
		print('servo', args)

class RelayNamespace(BaseNamespace):
	def on_command(self, *args):
		print('relay', args)


#logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
#logging.basicConfig()

socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)

if(ActionType.MOTION in CLIENT_MODES):
	motion_namespace = socketIO.define(MotionNamespace, '/motion')
if(ActionType.SERVO in CLIENT_MODES):
	servo_namespace = socketIO.define(ServoNamespace, '/servo')
if(ActionType.RELAY in CLIENT_MODES):
	relay_namespace = socketIO.define(RelayNamespace, '/relay')
#motion_namespace.send('command')

socketIO.wait()