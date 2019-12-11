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

    def saveOption(self, key: str, data):
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

    def loadOption(self, key: str):
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
    def setCameraUrl(self, url: str):
        if not url.strip():
            url = None
        self.saveOption('camera_url', url)

    def getCameraUrl(self) -> str:
        return self.loadOption('camera_url')

    # COMMANDS GRID
    def setCommandsGrid(self, grid: {}):
        self.saveOption('commands_grid', grid)

    def getCommandsGrid(self) -> {}:
        return self.loadOption('commands_grid')

    # AUDIO SOURCE
    def setAudioOnServer(self, mode: bool):
        self.saveOption('audio_on_server', mode)

    def getAudioOnServer(self) -> bool:
        mode = self.loadOption('audio_on_server')
        return mode or False

    # MOTION RASPI ID
    def setMotionRaspiId(self, raspi_id: str):
        if not raspi_id.strip():
            raspi_id = None
        self.saveOption('motion_raspi_id', raspi_id)

    def getMotionRaspiId(self) -> str:
        return self.loadOption('motion_raspi_id')

    # ROBOT NAME
    def setRobotName(self, name: str):
        if not name.strip():
            name = 'My robot'
        self.saveOption('robot_name', name)

    def getRobotName(self) -> str:
        name = self.loadOption('robot_name')
        return name or 'My robot'


class Resources():
    """
    Class used to store and manage ressources such as sounds or scripts
    """
    def __init__(self, scriptsPath, soundsPath):
        self.scriptsPath = scriptsPath
        self.soundsPath = soundsPath

    def getScripts(self):
        if not exists(self.scriptsPath):
            makedirs(self.scriptsPath)
        return [f for f in listdir(self.scriptsPath) if isfile(join(self.scriptsPath, f))]

    def deleteScript(self, script_name):
        path = join(self.scriptsPath, script_name)
        if isfile(path):
            remove(path)

    def saveScript(self, script_name, data):
        path = join(self.scriptsPath, script_name)
        with open(path, encoding='utf-8', mode='w+') as file:
            file.write(data)

    def readScript(self, script_name):
        path = join(self.scriptsPath, script_name)
        if not exists(path):
            return None
        with open(path, encoding='utf-8', mode='r') as file:
            return file.read()

    def getSounds(self):
        if not exists(self.soundsPath):
            makedirs(self.soundsPath)
        return [f for f in listdir(self.soundsPath) if isfile(join(self.soundsPath, f))]


config = CoreConfigFile(CONFIG_FILE)
resources = Resources(SCRIPTS_LOCATION, SOUNDS_LOCATION)
