from flask import Flask, render_template, Response
import cv2

# Define the base directory for your project
BASE_DIR = 'C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/'

# Initialize your Flask application
app = Flask(__name__, static_folder=BASE_DIR + '/static', template_folder=BASE_DIR + '/templates')

# Initialize video capture with cv2
capture = cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
