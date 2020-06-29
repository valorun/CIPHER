from . import armor


@armor.route('/armor')
def armor_page():
    return armor.render_page('armor.html')
