import cv2
import eel

# Initialize video capture
capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if not ret:
        break

    cv2.imshow('Processed Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()



# Assuming your 'web' directory is now structured like this:
# C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/web/index.html

eel.init('C:/src/Adafruit_WebSerial_3DModelViewer-master/Adafruit_WebSerial_3DModelViewer-master/')

@eel.expose
def my_python_function(param1):
    print(param1)

if __name__ == '__main__':
    eel.start('index.html', size=(800, 600))