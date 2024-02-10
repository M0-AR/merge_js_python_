import webview
import os


html_file_path = 'C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/index.html'

if __name__ == '__main__':
    if os.path.exists(html_file_path):
        # Create a webview window with the URL to the HTML file
        window = webview.create_window('3D Model Viewer', url=f'file:///{html_file_path}')
        webview.start(gui='edgechromium')
    else:
        print("HTML file not found at", html_file_path)