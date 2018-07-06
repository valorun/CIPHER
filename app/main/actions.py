#!/usr/bin/python
# coding: utf-8

import logging
import time
from flask import current_app
from .. import socketio, chatbot
import asyncio
from app.model import db, Relay

#classe permettant de lire une sequence ou d'executer une action
class SequenceReader:
	def __init__(self):
		#nombre d'actions en cours, qu'il faut donc attendre avant d'executer une autre séquence
		self.threads = 0

	#lance l'execution de la séquence,place chaque nouvelle branche dans un thread différent
	def executeSequence(self, app, startNode, nodes, edges):
		self.threads+=1
		self.executeAction(app, self.getNodeLabel(startNode, nodes))
		for c in self.getChildren(startNode, edges):
			socketio.start_background_task(self.executeSequence, app, c, nodes, edges)
		self.threads-=1

	#execute une action suivant un label donné, par exemple 'sleep:100ms'
	def executeAction(self, app, label):
		if(len(label.split(":"))<2):
			return
		action=label.split(":")[0]
		option=label.split(":")[1]
		if(action=="pause"):
			#si c'est une pause, l'execution du script se met en pause
			socketio.sleep( int(option.split("ms")[0])/1000 )
		elif(action=="speech"):
			#si c'est une parole, on retourne le tout directement au client
			socketio.emit("response", option.split('"')[0], namespace="/client")
		elif(action=="relay"): 
			#si c'est un relai, cherche d'abord le pin associé, reconstitue la requete
			rel_label=option.rsplit(',',1)[0]
			rel_state=""
			#si un état est spécifié (0 ou 1)
			if(len(option.rsplit(',',1))>1):
				rel_state=option.rsplit(',',1)[1]
			with app.app_context():
				db_rel = Relay.query.filter_by(label=rel_label).first()
				pin=db_rel.pin
				parity = db_rel.parity

				#si le relai est appairé
				if(parity!=""):
					#on récupère tout les relais pairs
					peers_rel = Relay.query.filter(Relay.parity==parity, Relay.label!=rel_label)
					peers=[]
					for peer in peers_rel:
						peers.append(peer.pin)

					socketio.emit("activate_paired_relay", (pin, rel_state, peers), namespace="/relay", broadcast=True)

				else:
					socketio.emit("activate_relay", (pin, rel_state), namespace="/relay")
				
		else:
			#envoie de la commande aux raspberries
			logging.info("Sending "+action+" to rasperries.")
			socketio.emit("command", option, namespace="/"+action)
		logging.info(label)

	#retourne la liste des id des noeuds enfants
	def getChildren(self, id, edges):
		children=[]
		for e in edges:
			if(e["from"]==id):
				children.append(e["to"])
		return children

	#retourne le label du noeud avec l'id donné
	def getNodeLabel(self, id, nodes):
		for n in nodes:
			if(n["id"]==id):
				return n["label"]

	def readSequence(self, app, json):
		if(self.threads>0): #on attend que la séquence en cours soit achevée pour en lancer une nouvelle
			return
		nodes=json[0]
		edges=json[1]
		self.executeSequence(app, "start", nodes, edges)


sequence_reader = SequenceReader()

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
