# ExE file is working as expected.
# pyinstaller --onefile main_08_combination_is_working.py
import cv2
import eel
import base64
import numpy as np
from threading import Thread
import time

eel.init('C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/')

def capture_stream():
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if ret:
            _, jpeg = cv2.imencode('.jpg', frame)
            jpeg_b64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')
            eel.updateImageSrc("data:image/jpeg;base64," + jpeg_b64)()
        else:
            break

@eel.expose
def start_stream():
    # Start the camera stream in a new thread to avoid blocking
    t = Thread(target=capture_stream)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    start_stream() # Start the camera stream
    eel.start('index.html', size=(1200, 1200))