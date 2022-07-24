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
    def_angle = db.Column(db.Integer, nullable=False)
    min_angle = db.Column(db.Integer, nullable=False)
    max_angle = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)
    raspi_id = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Servo %r>' % self.label


class Resources():
    """
    Class used to store and manage ressources such as sounds
    """
    def __init__(self, sounds_path: str):
        self.sounds_path = sounds_path
    def get_sounds(self):
        if not exists(self.sounds_path):
            makedirs(self.sounds_path)
        return [f for f in listdir(self.sounds_path) if isfile(join(self.sounds_path, f)) and f[0] != '.']

    def sound_exists(self, sound_name: str):
        return exists(self.get_sound_path(sound_name))

    def get_sound_path(self, sound_name: str):
        return join(self.sounds_path, sound_name)

    def write_sound(self, sound_name:str, sound: bytes):
        open(join(self.sounds_path, sound_name), 'wb').write(sound)

    def delete_sound(self, sound_name):
        if self.sound_exists(sound_name):
            remove(join(self.sounds_path, sound_name))

resources = Resources(core_config.SOUNDS_LOCATION)