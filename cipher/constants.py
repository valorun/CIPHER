import os

MQTT_BROKER_URL = 'localhost'
MQTT_BROKER_PORT = 1883

SERVER_DATABASE = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'server_data.db')

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

LOG_FILE = os.path.join(os.path.dirname(__file__), 'app.log')

SCRIPTS_LOCATION = os.path.join(os.path.dirname(__file__), 'scripts/')

SOUNDS_LOCATION = os.path.join(os.path.dirname(__file__), 'sounds/')

PLUGINS = ['dashboard', 'commands', 'speech', 'editor', 'debug', 'sequences', 'settings']  # all plugins to load, corresponds to the different pages available on the navbar
