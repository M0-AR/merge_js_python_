# pyinstaller --onefile --add-data "C:\src\merge_js_python\venv\Lib\site-packages\ultralytics\cfg\default.yaml;ultralytics\cfg" main.py
import cv2
import eel
import base64
import numpy as np
from threading import Thread
import time
from ultralytics import YOLO  # Ensure you have this installed

MODEL = "yolov8x.pt"
model = YOLO(MODEL)
model.fuse()
CLASS_NAMES_DICT = model.model.names
CLASS_ID = [2, 3, 5, 7]
video_path = 'test.mp4'

eel.init('C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/')


def capture_stream():
    capture = cv2.VideoCapture(video_path)
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        results = model.predict(frame, conf=0.5)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                conf = round(box.conf.item(), 2)
                cls = int(box.cls)
                label = f"{CLASS_NAMES_DICT[cls]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        jpeg_b64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')
        eel.updateImageSrc(f"data:image/jpeg;base64,{jpeg_b64}")()
        time.sleep(0.1)


@eel.expose
def start_stream():
    t = Thread(target=capture_stream)
    t.daemon = True
    t.start()


if __name__ == '__main__':
    start_stream()  # Start the video stream
    eel.start('index.html', size=(1200, 1200))

# is_server_started = False
#
# if __name__ == '__main__':
#     global is_server_started
#     if not is_server_started:
#         start_stream()  # Start the video stream
#         is_server_started = True
#         eel.start('index.html', size=(1200, 1200))
