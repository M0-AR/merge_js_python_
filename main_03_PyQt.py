import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def run(self):
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
            else:
                break
        capture.release()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Web view
        self.web_view = QWebEngineView()
        self.web_view.load(
            QUrl("C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/index.html"))
        layout.addWidget(self.web_view)

        # Label for video
        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setWindowTitle("Camera and 3D Model Viewer")

    def set_image(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()

    # Start video thread
    video_thread = VideoThread()
    video_thread.change_pixmap_signal.connect(main_window.set_image)
    video_thread.start()

    sys.exit(app.exec_())
