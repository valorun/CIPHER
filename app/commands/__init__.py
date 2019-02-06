from flask import Blueprint

commands = Blueprint('commands', __name__, static_folder='static', static_url_path='/commands/static', template_folder='templates')

from . import routes, events
