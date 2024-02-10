# I suggested PyQt over Tkinter primarily because PyQt offers a more advanced set of GUI components,
# including WebEngineView, which can render modern web content including HTML5, CSS3, and JavaScript. This is not
# inherently possible with Tkinter, as it doesn't have a built-in widget for rendering web pages to the same degree.
# PyQt's WebEngineView is based on Chromium and thus supports a wide range of web technologies that are crucial for
# embedding complex web content such as 3D models or WebGL-based applications.
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2

# Function to update the image on the label
def show_frame():
    _, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lblVideo.imgtk = imgtk
    lblVideo.configure(image=imgtk)
    lblVideo.after(10, show_frame)

# Exit function to properly release the video capture object
def on_closing():
    capture.release()
    window.destroy()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Tkinter and OpenCV")
    lblVideo = Label(window)
    lblVideo.pack()

    capture = cv2.VideoCapture(0)

    # Call the function to update frames
    show_frame()

    # Set a callback for when the window is closed
    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()
