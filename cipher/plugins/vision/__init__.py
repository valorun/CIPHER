from cipher.plugins import Plugin

vision = Plugin('vision', __name__, 'Vision', 'fa-eye')

from . import routes, actions, events
