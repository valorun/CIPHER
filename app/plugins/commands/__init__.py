from app.plugins import Plugin

commands = Plugin('commands', __name__, 'Commandes manuelles', 'fa-terminal')

from . import routes, events
