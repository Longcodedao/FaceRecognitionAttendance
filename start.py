import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import face_recognition

class WebcamApp:
    def __init__(self, window, window_title, name):
        self.name = name
        self.number_capture = 0

        self.window = window
        self.window.title(window_title)

        self.video_source = 1
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.has_captured = False

        self.canvas = tk.Canvas(window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack()

        btn_style = ttk.Style()
        btn_style.configure("TButton", font=("Helvetica", 12, "bold"), foreground="blue")

        self.btn_capture = ttk.Button(window, text="Capture", command=self.capture_image)
        self.btn_capture.pack()
        
        # Bind the Esc Key to close the window
        self.window.bind('<Escape>', self.close_window)
        self.setup_folder()
        self.update()

        self.window.mainloop()


    def setup_folder(self):
        image_path = os.path.join(os.getcwd(), 'other_db', self.name)
        if (not os.path.exists(image_path)):
            os.makedirs(image_path)
            print('Creating the folder')

        self.path_save = image_path


    def capture_image(self):
        ret, frame = self.vid.read()
        if ret:
            if (self.has_captured):
                cv2.imwrite(f"{os.path.join(self.path_save, f'{self.number_capture}.jpg')}", frame)
                print(f"Image captured and saved as {self.number_capture}.jpg")
                self.number_capture += 1
            else:
                print("Cannot capture the file image")


    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            face_locations = face_recognition.face_locations(frame)
            print(face_locations)

            if (face_locations):
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                self.has_captured = True
            else:
                self.has_captured = False

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def close_window(self, event):
        self.window.destroy()

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a Tkinter window

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please input your name")
        sys.exit(1)

    folder_path = sys.argv[1]

    root = tk.Tk()
    app = WebcamApp(root, "Webcam App", folder_path)