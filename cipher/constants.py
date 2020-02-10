from os.path import join, dirname

MQTT_BROKER_URL = 'localhost'
MQTT_BROKER_PORT = 1883

SERVER_DATABASE = 'sqlite:///' + join(dirname(__file__), 'server_data.db')

CONFIG_FILE = join(dirname(__file__), 'config.json')

LOG_FILE = join(dirname(__file__), 'app.log')

SCRIPTS_LOCATION = join(dirname(__file__), 'scripts/')

SOUNDS_LOCATION = join(dirname(__file__), 'sounds/')

PLUGINS = ['dashboard', 'commands', 'speech', 'editor', 'debug', 'sequences', 'armor', 'settings']  # all plugins to load, corresponds to the different pages available on the navbar
