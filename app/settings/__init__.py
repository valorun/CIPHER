from flask import Blueprint

settings = Blueprint('settings', __name__, static_folder='static', static_url_path='/settings/static', template_folder='templates')

from . import routes
