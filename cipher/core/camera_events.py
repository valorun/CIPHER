import json
import base64
from flask_socketio import SocketIO, emit
from cipher import socketio, mqtt
from cipher.model import core_config
from . import core
from .camera import camera
#import picamera 

streaming = False

@socketio.on('stop_camera_stream', namespace='/client')
def stop_camera_stream():
    global streaming
    streaming = False
    socketio.emit('stopped_camera_stream', namespace="/client", broadcast=True)
    core.log.info("Stopped camera streaming.")

@socketio.on('start_camera_stream', namespace='/client')
def start_camera_stream():
    global streaming
    if not camera.is_opened():
        camera.open()
    streaming = True
    socketio.start_background_task(send_camera_data)
    socketio.emit('started_camera_stream', namespace="/client", broadcast=True)
    core.log.info("Started camera streaming.")


def send_camera_data():
    while streaming:
        jpeg = camera.get_jpeg_frame()
        jpeg = jpeg.tobytes()
        jpeg = base64.b64encode(jpeg).decode('utf-8')
        socketio.emit('camera_stream_data', 'data:image/jpeg;base64,{}'.format(jpeg), namespace="/client", broadcast=True)
        socketio.sleep(core_config.CAMERA_FRAME_RATE / 60)
    camera.release()

        