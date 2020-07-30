from cv2 import cv2

class Camera():
    def __init__(self):
        self.vc = cv2.VideoCapture(0)
        self.post_process = []
        self.opened = False

    def get_frame(self):
        if not self.is_opened():
            return
        rval, frame = self.vc.read()
        for p in self.post_process:
            p(frame)
        return frame
    
    def get_jpeg_frame(self):
        ret, jpeg = cv2.imencode('.jpg', self.get_frame())
        return jpeg

    def is_opened(self):
        return (self.vc is not None and self.vc.isOpened()) and self.opened
    
    def release(self):
        self.vc.release()
        self.opened = False

    def add_processing(self, func):
        if callable(func):
            self.post_process.append(func)
            return True
        return False
    
    def open(self):
        if self.vc is None:
            return False
        self.vc.open(0)
        self.opened = True
        return True

camera = Camera()