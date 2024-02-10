from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO  # Ensure you have this installed

# Define the base directory for your project
BASE_DIR = 'C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/'

# Initialize your Flask application
app = Flask(__name__, static_folder=BASE_DIR + '/static', template_folder=BASE_DIR + '/templates')

MODEL = "yolov8x.pt"
model = YOLO(MODEL)
model.fuse()
CLASS_NAMES_DICT = model.model.names

video_path = 'test.mp4'
def gen_frames():  # Generate frame by frame from camera
    capture = cv2.VideoCapture(video_path)
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            results = model.predict(frame, conf=0.5)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                    conf = round(box.conf.item(), 2)
                    cls = int(box.cls)
                    label = f"{CLASS_NAMES_DICT[cls]} {conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
