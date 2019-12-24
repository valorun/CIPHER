from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import listdir, makedirs, remove
from os.path import isfile, join, exists
from .constants import CONFIG_FILE, SCRIPTS_LOCATION, SOUNDS_LOCATION
import json

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


class ConfigFile():
    """
    Class used to generate and manage a config file
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def save_option(self, key: str, data):
        """
        Save an option into the config file.
        """
        try:
            with open(self.filepath, 'r') as f:
                content = json.load(f)
        except IOError:  # if no file exists, or if the data is not in json
            with open(self.filepath, 'w') as f:
                f.write("")  # create a new one
            content = {}
        except ValueError:
            content = {}
        content[key] = data
        with open(self.filepath, 'w') as f:
            json.dump(content, f)

    def load_option(self, key: str):
        """
        Load an option from the config file.
        """
        try:
            with open(self.filepath, 'r') as f:
                content = json.load(f)
                option = content[key]
        except (IOError):
            with open(self.filepath, 'w') as f:
                f.write("")
            option = None
        except (KeyError, ValueError):
            option = None
        return option


class CoreConfigFile(ConfigFile):

    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)

    # CAMERA URL
    def set_camera_url(self, url: str):
        if not url.strip():
            url = None
        self.save_option('camera_url', url)

    def get_camera_url(self) -> str:
        return self.load_option('camera_url')

    # AUDIO SOURCE
    def set_audio_on_server(self, mode: bool):
        self.save_option('audio_on_server', mode)

    def get_audio_on_server(self) -> bool:
        mode = self.load_option('audio_on_server')
        return mode or False

    # MOTION RASPI ID
    def set_motion_raspi_id(self, raspi_id: str):
        if not raspi_id.strip():
            raspi_id = None
        self.save_option('motion_raspi_id', raspi_id)

    def get_motion_raspi_id(self) -> str:
        return self.load_option('motion_raspi_id')

    # ROBOT NAME
    def set_robot_name(self, name: str):
        if not name.strip():
            name = 'My robot'
        self.save_option('robot_name', name)

    def get_robot_name(self) -> str:
        name = self.load_option('robot_name')
        return name or 'My robot'


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


config = CoreConfigFile(CONFIG_FILE)
resources = Resources(SCRIPTS_LOCATION, SOUNDS_LOCATION)
