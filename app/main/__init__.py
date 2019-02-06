from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, events, raspies_events, action_events
