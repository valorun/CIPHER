from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, commands, sequences, settings, events, raspies_events, speech_events, commands_events, actions
