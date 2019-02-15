from app.plugins import Plugin

dashboard = Plugin('dashboard', __name__, 'Tableau de bord', 'fa-tachometer-alt')

from . import routes
