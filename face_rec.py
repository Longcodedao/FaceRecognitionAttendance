import cv2
import numpy as np
from utils import *
from gtts import gTTS
from playsound import playsound
import os
import uuid
import time

for name, img_path in img_paths.items():
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    _, img_shapes, _ = find_faces(img_rgb)
    descs[name] = encode_faces(img_rgb, img_shapes)[0]
np.save('img/descs.npy', descs) 

# Load saved descriptors
descs = np.load('img/descs.npy', allow_pickle=True).item()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# 웹캠 초기화 여부 확인 변수
webcam_initialized = True

print("starting!!")

detecting_faces = True

while cap.isOpened():
    print("detecting face.....")

    if not webcam_initialized:
        ret, img = cap.read()

        if not ret:
            print("Failed to capture frame from webcam.")
            break

        webcam_initialized = True

    ret, img = cap.read()

    if not ret:
        print("Failed to capture frame from webcam.")
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if detecting_faces:
        # Find faces in the image
        rects, shapes, _ = find_faces(img_rgb)
        descriptors = encode_faces(img_rgb, shapes)

        found = False  # Initialize the 'found' variable

        for i, desc in enumerate(descriptors):
            for name, saved_desc in descs.items():
                dist = np.linalg.norm([desc] - saved_desc, axis=1)
                if dist < 0.6:
                    found = True
                    cv2.rectangle(img, (rects[i][0][0], rects[i][0][1]), 
                                  (rects[i][1][0], rects[i][1][1]), (0, 255, 0), 2)
                    cv2.putText(img, name, (rects[i][0][0], rects[i][0][1] - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    # Generate and play the greeting audio
                    unique_filename = str(uuid.uuid4())
                    file_path = f"audio/greeting_{name}_{unique_filename}.mp3"
                    tts = gTTS(f"Hello {name}! Welcome!")
                    tts.save(file_path)
                    playsound(file_path)
                    os.remove(file_path)  # 파일 삭제

                    break

            if found:
                break

        if not found:
            for i, _ in enumerate(descriptors):
                cv2.rectangle(img, (rects[i][0][0], rects[i][0][1]), 
                              (rects[i][1][0], rects[i][1][1]), (0, 0, 255), 2)
                cv2.putText(img, "Unknown", (rects[i][0][0], rects[i][0][1] - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # Generate and play the unknown person audio
                tts_unknown = gTTS("Unknown: Who are you?")
                tts_unknown.save("audio/unknown_person.mp3")
                playsound("audio/unknown_person.mp3")
                os.remove("audio/unknown_person.mp3")

        cv2.imshow('Face Recognition', img)

    else:
        print("Press 'out!' to go back to face detection.")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
