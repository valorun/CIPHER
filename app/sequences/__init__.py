from flask import Blueprint

sequences = Blueprint('sequences', __name__, static_folder='static', static_url_path='/sequences/static', template_folder='templates')

from . import routes
