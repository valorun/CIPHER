from flask_sqlalchemy import SQLAlchemy
from os import listdir, makedirs, remove
from os.path import isfile, join, exists
from .config import core_config

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


resources = Resources(core_config.SCRIPTS_LOCATION, core_config.SOUNDS_LOCATION)