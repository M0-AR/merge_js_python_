import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtWebKit import QWebSettings


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Web view
        self.view = QWebView(self)
        self.view.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.view.load(QUrl(
            "file:///C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/index.html"))
        layout.addWidget(self.view)

        # Web inspector
        self.inspector = QWebInspector()
        self.inspector.setPage(self.view.page())
        self.inspector.show()

        # Splitter to contain the web view and the inspector
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.inspector)

        # Adding splitter to layout
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        self.setWindowTitle("Camera and 3D Model Viewer")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())
