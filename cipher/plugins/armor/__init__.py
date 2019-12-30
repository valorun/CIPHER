from cipher.plugins import Plugin
from cipher.model import db

armor = Plugin('armor', __name__, 'Mode armure', 'fa-user-astronaut')

from . import routes
