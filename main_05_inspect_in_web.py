# https://stackoverflow.com/questions/41432898/implementing-web-inspection-in-browser-using-pyqt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.view = QWebView(self)
        self.view.settings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True)
        self.inspector = QWebInspector()
        self.inspector.setPage(self.view.page())
        self.inspector.show()
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.inspector)
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.view.load(QUrl('http://www.google.com'))
    window.show()
    sys.exit(app.exec_())