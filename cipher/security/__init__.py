from flask import Blueprint

security = Blueprint('security', __name__)

from . import routes
from .decorators import login_required
