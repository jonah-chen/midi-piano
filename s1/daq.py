from threading import Thread
from cv2 import cv2

class VideoGet:
    """ Uses threading to get video from the webcam pretty quickly
    """
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, 1280)
        self.stream.set(4, 720)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    
    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True