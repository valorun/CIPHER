from flask_sqlalchemy import SQLAlchemy
from os import listdir, makedirs, remove
from os.path import isfile, join, exists, dirname
from .constants import CONFIG_FILE
from configparser import ConfigParser

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Sequence(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Sequence %r>' % self.id


class Relay(db.Model):
    label = db.Column(db.String(50), primary_key=True)
    pin = db.Column(db.String(4), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)
    parity = db.Column(db.String(20), nullable=False)
    raspi_id = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Relay %r>' % self.label


class Servo(db.Model):
    label = db.Column(db.String(50), primary_key=True)
    pin = db.Column(db.String(4), nullable=False)
    def_pulse_width = db.Column(db.Integer, nullable=False)
    min_pulse_width = db.Column(db.Integer, nullable=False)
    max_pulse_width = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)
    raspi_id = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Servo %r>' % self.label

class ConfigFile(ConfigParser):
    """
    Class used to generate and manage a config file
    """
    def __init__(self, filepath):
        ConfigParser.__init__(self)
        self.filepath = filepath
        if exists(filepath):
            self.read(filepath)

    def set(self, section: str, option: str, data):
        """
        Save an option into the config file.
        """
        self.set(section, option, data)
        with open(self.filepath, 'w') as f:
            self.write(f)


class CoreConfig(ConfigFile):

    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)

    # MQTT BROKER URL
    def get_mqtt_broker_url(self):
        return self.get('MQTT_BROKER', 'URL', fallback='localhost')

    # MQTT BROKER PORT
    def get_mqtt_broker_port(self):
        return self.get('MQTT_BROKER', 'PORT', fallback=1883)

    # SERVER DATABASE
    def get_database_file(self):
        return self.get('SERVER', 'DATABASE_FILE', fallback='sqlite:///' + join(dirname(__file__), 'server_data.db'))

    # LOG FILE
    def get_log_file(self):
        return self.get('SERVER', 'LOG_FILE', fallback=join(dirname(__file__), 'app.log'))

    # SCRIPTS LOCATION
    def get_scipts_location(self):
        return self.get('SERVER', 'SCRIPTS_LOCATION', fallback=join(dirname(__file__), 'scripts/'))

    # SOUNDS LOCATION
    def get_sounds_location(self):
        return self.get('SERVER', 'SOUNDS_LOCATION', fallback=join(dirname(__file__), 'sounds/'))

    # PLUGINS
    def get_plugins(self):
        return self.get('SERVER', 'PLUGINS', fallback=['dashboard', 'commands', 'speech', 'editor', 'debug', 'sequences', 'armor', 'settings'])  # all plugins to load, corresponds to the different pages available on the navbar

    # CAMERA URL
    def set_camera_url(self, url: str):
        if not url.strip():
            url = None
        self.set('GENERAL', 'CAMERA_URL', url)

    def get_camera_url(self) -> str:
        return self.get('GENERAL', 'CAMERA_URL', fallback=None)

    # AUDIO SOURCE
    def set_audio_on_server(self, mode: bool):
        self.set('GENERAL', 'AUDIO_ON_SERVER', mode)

    def get_audio_on_server(self) -> bool:
        return self.getboolean('GENERAL', 'AUDIO_ON_SERVER', fallback=False)

    # MOTION RASPI ID
    def set_motion_raspi_id(self, raspi_id: str):
        if not raspi_id.strip():
            raspi_id = None
        self.set('GENERAL', 'MOTION_RASPI_ID', raspi_id)

    def get_motion_raspi_id(self) -> str:
        return self.get('GENERAL', 'MOTION_RASPI_ID', fallback=None)

    # ROBOT NAME
    def set_robot_name(self, name: str):
        if not name.strip():
            name = 'My robot'
        self.set('GENERAL', 'ROBOT_NAME', name)

    def get_robot_name(self) -> str:
        return self.get('GENERAL', 'ROBOT_NAME', fallback='My robot')

    # DEBUG
    def get_debug_mode(self) -> bool:
        return self.getboolean('SERVER', 'DEBUG', fallback=False)


class Resources():
    """
    Class used to store and manage ressources such as sounds or scripts
    """
    def __init__(self, scripts_path, sounds_path):
        self.scripts_path = scripts_path
        self.sounds_path = sounds_path

    def get_scripts(self):
        if not exists(self.scripts_path):
            makedirs(self.scripts_path)
        return [f for f in listdir(self.scripts_path) if isfile(join(self.scripts_path, f))]

    def delete_script(self, script_name):
        path = join(self.scripts_path, script_name)
        if isfile(path):
            remove(path)

    def save_script(self, script_name, data):
        path = join(self.scripts_path, script_name)
        with open(path, encoding='utf-8', mode='w+') as file:
            file.write(data)

    def read_script(self, script_name):
        path = join(self.scripts_path, script_name)
        if not exists(path):
            return None
        with open(path, encoding='utf-8', mode='r') as file:
            return file.read()

    def get_sounds(self):
        if not exists(self.sounds_path):
            makedirs(self.sounds_path)
        return [f for f in listdir(self.sounds_path) if isfile(join(self.sounds_path, f))]


config = CoreConfig(CONFIG_FILE)
resources = Resources(config.get_scipts_location(), config.get_sounds_location())
