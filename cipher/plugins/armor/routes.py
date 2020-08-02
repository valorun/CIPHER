from . import armor
from cipher import SocketIOHandler


@armor.route('/armor')
def armor_page():
    log_records = '\n'.join(SocketIOHandler.log_queue) + '\n'
    return armor.render_page('armor.html', log_records=log_records)
