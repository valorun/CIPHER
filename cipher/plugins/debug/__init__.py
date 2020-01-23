from cipher.plugins import Plugin
from cipher.model import db

debug = Plugin('debug', __name__, 'Panneau de debug', 'fa-bug')

from . import routes
