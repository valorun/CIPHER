import os

SERVER_DATABASE='sqlite:///' + os.path.join(os.path.dirname(__file__), 'server_data.db')

KEYWORDS_DATASET=os.path.join(os.path.dirname(__file__),"keywords_dataset.json")

COMMANDS_GRID=os.path.join(os.path.dirname(__file__),"commands_grid.json")

CHATBOT_DATABASE=os.path.join(os.path.dirname(__file__),"chatbot/chatbot.db")

SCRIPTS_LOCATION=os.path.join(os.path.dirname(__file__),"scripts/")

SOUNDS_LOCATION=os.path.join(os.path.dirname(__file__),"sounds/")
