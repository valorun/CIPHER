from flask import Blueprint

debug = Blueprint('debug', __name__, static_folder='static', static_url_path='/debug/static', template_folder='templates')

from . import routes
