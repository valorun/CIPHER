#!/usr/bin/python
# coding: utf-8

import logging
from chatterbot import ChatBot

class ChatBotWrapper():

    def __init__(self, database):
        self.chatbot = None
        self._readOnly = False
        self.database=database

    def instantiateChatBot(self, readOnly: bool, corpusTrainer: bool=False):
        self._readOnly = readOnly
        if corpusTrainer:
            selectedTrainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
        else:
            selectedTrainer = 'chatterbot.trainers.ListTrainer'
        self.chatbot = ChatBot(
            'Hector',
            trainer=selectedTrainer,
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
            read_only=readOnly,
            database=self.database
        )
    
    def getResponse(self, statement):
        return self.chatbot.get_response(statement)
    
    #train the chatbot on a already existing corpus
    def trainOnCorpus(self, corpusPath):
        logging.info("Chatbot trained with corpus: ".join(corpusPath))
        readOnly=self._readOnly
        self.instantiateChatBot(False, True)
        self.chatbot.train(corpusPath)
        self.instantiateChatBot(readOnly)

    #train the chatbot on a conversation represented as a list of sentences
    def train(self, conversation: []):
        logging.info("Chatbot trained with conversation: ".join(conversation))
        readOnly=self._readOnly
        self.instantiateChatBot(False)
        self.chatbot.train(conversation)
        self.instantiateChatBot(readOnly)