import os

MQTT_BROKER_URL='localhost'#'192.168.1.27'
MQTT_BROKER_PORT=1883

SERVER_DATABASE='sqlite:///' + os.path.join(os.path.dirname(__file__), 'server_data.db')

CONFIG_FILE=os.path.join(os.path.dirname(__file__),'config.json')

LOG_FILE=os.path.join(os.path.dirname(__file__),'app.log')

SCRIPTS_LOCATION=os.path.join(os.path.dirname(__file__),'scripts/')

SOUNDS_LOCATION=os.path.join(os.path.dirname(__file__),'sounds/')