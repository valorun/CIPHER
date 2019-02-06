from flask import Blueprint

dashboard = Blueprint('dashboard', __name__, static_folder='static', static_url_path='/dashboard/static', template_folder='templates')

from . import routes
