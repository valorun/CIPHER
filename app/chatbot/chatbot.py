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
        """
        Instanciate the chatbot.
        """
        self._readOnly = readOnly
        logging.info("Instantiating new chatbot")
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
        """
        Get the best response to a given statement.
        """
        return self.chatbot.get_response(statement)
    
    def trainOnCorpus(self, corpusPath):
        """
        Train the chatbot on an already existing corpus.
        """
        logging.info("Chatbot trained with corpus: ".join(corpusPath))
        readOnly=self._readOnly
        self.instantiateChatBot(False, True)
        self.chatbot.train(corpusPath)
        self.instantiateChatBot(readOnly)

    def train(self, conversation: []):
        """
        Train the chatbot on a conversation represented as a list of sentences.
        """
        logging.info("Chatbot trained with conversation: ".join(conversation))
        readOnly=self._readOnly
        self.instantiateChatBot(False)
        self.chatbot.train(conversation)
        self.instantiateChatBot(readOnly)