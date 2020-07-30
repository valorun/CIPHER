from cv2 import cv2
from os.path import join, dirname
import numpy as np

YOLO_WEIGHTS_PATH = join(dirname(__file__), 'yolov3.weights')
YOLO_CLASSES_PATH = join(dirname(__file__), 'yolov3.classes')
YOLO_CONFIG_PATH = join(dirname(__file__), 'yolov3.cfg')

CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

CLASSES = None
with open(YOLO_CLASSES_PATH, 'r') as f:
    CLASSES = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

def detect_objects(frame):
    width = frame.shape[1]
    height = frame.shape[0]

    def get_output_layers(net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    net = cv2.dnn.readNet(YOLO_WEIGHTS_PATH, YOLO_CONFIG_PATH)
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416,416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)
    indices = indices.flatten()

    return indices, class_ids, boxes, confidences

def list_objects(frame):
    indices, class_ids, boxes, confidences = detect_objects(frame)
    return [CLASSES[class_ids[i]] for i in indices]

def draw_objects(frame):
    indices, class_ids, boxes, confidences = detect_objects(frame)

    def draw(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = "{}: {:.4f}".format(CLASSES[class_id], confidence)
        color = COLORS[class_id]
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw(frame, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
    return frame