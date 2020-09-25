from cipher import mqtt, socketio
from flask_mqtt import Mqtt

from . import vision


@mqtt.on_topic('server/camera_stream/frame')
def on_camera_stream(client, userdata, msg):
    """
    Function called when a frame is captured by the camera.
    """
    vision.log.debug("Received camera frame.")
    socketio.emit('camera_stream_data', msg.payload.decode('utf-8'), namespace="/client", broadcast=True)

@mqtt.on_topic('server/objects_detected')
def on_objects_detected(client, userdata, msg):
    """
    Function called when the camera detected some object.
    """
    socketio.emit('camera_objects_detected', 'data:image/jpeg;base64,{}'.format(msg), namespace="/client", broadcast=True)

@mqtt.on_topic('server/camera_stream/started')
def on_started_camera_stream(client, userdata, msg):
    socketio.emit('started_camera_stream', namespace='/client', broadcast=True)
    vision.log.info("Camera streaming successfully started.")

@mqtt.on_topic('server/camera_stream/stopped')
def on_stopped_camera_stream(client, userdata, msg):
    socketio.emit('stopped_camera_stream', namespace='/client', broadcast=True)
    vision.log.info("Camera streaming successfully stopped.")

@socketio.on('stop_camera_stream', namespace='/client')
def stop_camera_stream():
    mqtt.publish('client/vision/stop')
    vision.log.info("Stopped camera streaming.")

@socketio.on('start_camera_stream', namespace='/client')
def start_camera_stream():
    mqtt.publish('client/vision/start')
    vision.log.info("Started camera streaming.")