from cipher.security import login_required
from . import vision


@vision.route('/vision')
@login_required
def debug_page():
	return vision.render_page('vision.html')

#camera.add_processing(draw_objects)