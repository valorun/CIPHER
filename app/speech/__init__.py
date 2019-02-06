from flask import Blueprint

speech = Blueprint('speech', __name__, static_folder='static', static_url_path='/speech/static', template_folder='templates')

from . import routes, events
