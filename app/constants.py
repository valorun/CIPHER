import os

SERVER_DATABASE='sqlite:///' + os.path.join(os.path.dirname(__file__), 'server_data.db')

CONFIG_FILE=os.path.join(os.path.dirname(__file__),"config.json")

LOG_FILE=os.path.join(os.path.dirname(__file__),"app.log")

CHATBOT_DATABASE=os.path.join(os.path.dirname(__file__),"chatbot/chatbot.db")

SCRIPTS_LOCATION=os.path.join(os.path.dirname(__file__),"scripts/")

SOUNDS_LOCATION=os.path.join(os.path.dirname(__file__),"sounds/")
