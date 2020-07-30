from cipher.core.camera import camera
from cipher.security import login_required
from . import vision
from .object_detection import draw_objects


@vision.route('/vision')
@login_required
def debug_page():
	return vision.render_page('vision.html')

#camera.add_processing(draw_objects)