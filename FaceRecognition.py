import tkinter as tk
from tkinter import messagebox

import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk
import os

import asyncio
import aiohttp


#ai speaker import
import uuid
import time
from playsound import playsound
from gtts import gTTS


class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        self.known_encodings = []
        self.known_names = []

        self.capture = None

        self.recognize_names = "Unknown"

        self.load_known_faces()

        # self.cap = cv2.VideoCapture(1)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # Set width to 640
        self.cap.set(4, 480)  # Set height to 480

        self.process_this_frame = True

        self.label = tk.Label(root)
        self.label.grid(row = 0)

        # Name label pack
        self.class_label = tk.Label(root, text="Class for Taking Attendance:")
        self.class_label.grid(row = 0, column = 2, padx=10, sticky="e")

        self.class_entry = tk.Entry(root)
        self.class_entry.grid(row = 0, column = 3, padx=10, sticky="w")


        # Capture button
        self.capture_button = tk.Button(root, text="Capture", command=self.capture_frame)
        self.capture_button.grid(row = 2)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.grid(row = 3)

        self.quit_button = tk.Button(root, text="Quit", command=self.quit)
        self.quit_button.grid(row = 4)

        self.loop = asyncio.get_event_loop()

        self.update()

    def load_known_faces(self):
        # os.chdir('data/images')'
        data_path = './data/images'
        for folder in os.listdir(data_path):
            for file in os.listdir(os.path.join(data_path, folder)):
                image_path = os.path.join(data_path, folder, file)
                known_img = face_recognition.load_image_file(image_path)
                known_encoding = face_recognition.face_encodings(known_img)[0]
                self.known_encodings.append(known_encoding)
                self.known_names.append(folder)

    def update(self):
        ret, frame = self.cap.read()
        face_locations = []
        face_encodings = []
        face_names = []

        if ret:
            frame = cv2.flip(frame, 1)

            if self.process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5).astype(np.uint8)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    print(face_distances)
                    if matches[best_match_index] and face_distances[best_match_index] <= 0.45:
                        self.recognize_names = self.known_names[best_match_index]
                    else:
                        self.recognize_names = "Unknown"
                    face_names.append(self.recognize_names)

            self.process_this_frame = not self.process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                if name != "Unknown":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.putText(frame, self.recognize_names, (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            photo = self.convert_frame_to_photo(frame)
            self.label.config(image=photo)
            self.label.image = photo

        self.root.after(1, self.update)

    def convert_frame_to_photo(self, frame):
        return ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

    def capture_frame(self):
        ret, frame = self.cap.read()
        if  ret and self.recognize_names != "Unknown":
            self.capture = frame
            # asyncio.run(self.send_name_to_server(self.recognize_names, self.class_entry.get()))
            asyncio.run(self.send_name_to_server(self.recognize_names, self.class_entry.get()))
        
        self.recognize_names = "Unknown"

    def reset(self):
        self.recognize_names = "Unknown"

    def play_text_to_speech_welcome(self, text):
        tts = gTTS(text)
        tts.save("./samplesound/welcome.mp3")  # Save the generated speech as an audio file
        playsound("./samplesound/welcome.mp3")  # Play the audio file
        os.remove("./samplesound/welcome.mp3")

    def play_text_to_speech_unknown(self, text):
        tts = gTTS(text)
        tts.save("./samplesound/unknown_person.mp3")
        playsound("./samplesound/unknown_person.mp3")
        os.remove("./samplesound/unknown_person.mp3")


        
    async def send_name_to_server(self, name, classroom):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:5000/recognized_person", 
                                        json = {"name": name, "classroom": classroom}) as response:
                    if response.status == 200:
                        result = await response.json()
                        welcome_text = f"Welcome to {self.class_entry.get()}. Hello {self.recognize_names}"
                        self.play_text_to_speech_welcome(welcome_text)
                        messagebox.showinfo("Success", "Attendance Checked")
                    else:
                        unknown_text=f"Who are you? Please recapture your picture"
                        self.play_text_to_speech_unknown(unknown_text)
                        messagebox.showerror("Error", "Failed")

        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")

        # url = "http://localhost:5000/recognized_person"
        # # response = await self.loop.run_in_executor(None, lambda: requests.post(url, data= {"name": name, "classroom": classroom}))
        # # self.print_response(response.text)
        # response = requests.post(url, data = {"name": name, "classroom": classroom})
        # print(response.text)

    def print_response(self, response_text):
        print(response_text)


    def quit(self):
        self.cap.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
    cv2.destroyAllWindows()