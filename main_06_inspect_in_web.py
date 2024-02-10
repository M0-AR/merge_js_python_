import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMenu
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtWebKit import QWebSettings
# from PyQt5.QtWebEngineWidgets import QWebEngineView


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
        self.view = QWebView(self)
        # self.web_view = QWebEngineView()
        self.view.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.view.load(QUrl(
            "file:///C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/index.html"))
        layout.addWidget(self.view)

        self.inspector = QWebInspector()
        self.inspector.setPage(self.view.page())
        self.inspector.show()
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.inspector)
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)


        # Label for video
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # # Set up context menu for the web view
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.on_context_menu)

        self.setLayout(layout)
        self.setWindowTitle("Camera and 3D Model Viewer")

    def on_context_menu(self, point):
        context_menu = QMenu()
        inspect_action = context_menu.addAction("Inspect Element")
        action = context_menu.exec_(self.view.mapToGlobal(point))
        if action == inspect_action:
            self.inspect_element_at_point(point)

    def inspect_element_at_point(self, point):
        page = self.view.page()
        page.runJavaScript(f'inspect(document.elementFromPoint({point.x()}, {point.y()}));')

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
