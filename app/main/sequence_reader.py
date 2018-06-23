#!/usr/bin/python
# coding: utf-8

import time
from .. import socketio
import asyncio
from app.model import db, Relay

#classe permettant de lire une sequence ou d'executer une action
class SequenceReader:
	def __init__(self):
		#nombre d'actions en cours, qu'il faut donc attendre avant d'executer une autre séquence
		self.threads = 0

	#lance l'execution de la séquence,place chaque nouvelle branche dans un thread différent
	def executeSequence(self, startNode, nodes, edges):
		self.threads+=1
		self.executeAction(self.getNodeLabel(startNode, nodes))
		for c in self.getChildren(startNode, edges):
			socketio.start_background_task(self.executeSequence, c, nodes, edges)
		self.threads-=1

	#execute une action suivant un label donné, par exemple 'sleep:100ms'
	def executeAction(self, label):
		if(len(label.split(":"))<2):
			return
		action=label.split(":")[0]
		option=label.split(":")[1]
		if(action=="pause"):
			#si c'est une pause, l'execution du script se met en pause
			socketio.sleep( int(option.split("ms")[0])/1000 )
		elif(action=="speech"):
			#si c'est une parole, on retourne le tout directement au client
			socketio.emit("response", option.split('"')[0], namespace="/client", broadcast=True)
		elif(action=="relay"): 
			#si c'est un relai, cherche d'abord le pin associé, reconstitue la requete
			rel_label=option.rsplit(',',1)[0]
			rel_state=""
			#si un état est spécifié (0 ou 1)
			if(len(option.rsplit(',',1))>1):
				rel_state=','+option.rsplit(',',1)[1]
			db_rel = Relay.query.filter_by(label=rel_label).first()
			socketio.emit("command", (db_rel.pin, rel_state), namespace="/relay", broadcast=True)
		else:
			#envoie de la commande aux raspberries
			print("Sending "+action+" to rasperries.")
			socketio.emit("command", option, namespace="/"+action, broadcast=True)
		print(label)

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

	def readSequence(self, json):
		if(self.threads>0): #on attend que la séquence en cours soit achevée pour en lancer une nouvelle
			return
		nodes=json[0]
		edges=json[1]
		self.executeSequence("start", nodes, edges)
