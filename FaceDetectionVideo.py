import face_recognition
import cv2
import os
import numpy as np

known_encodings = []
known_names = []

os.chdir('other_db')

# Load images from the specified folders
for folder in os.listdir():
    print(os.listdir(folder))
    for file in os.listdir(folder):
        
        image_path = os.path.join(folder, file)
        known_img = face_recognition.load_image_file(image_path)
        # known_image = face_recognition.load_image_file(image_path)
        # print(face_recognition.face_encodings(known_image))
        known_encoding = face_recognition.face_encodings(known_img)[0]
        known_encodings.append(known_encoding)
        known_names.append(folder)    

cap = cv2.VideoCapture(1)
process_this_frame = True

width = 1280
height = 720 


while True:
    ret, frame = cap.read()

    if not ret:
        print("Shutdown!!!")
        break
    frame = cv2.flip(frame, 1)

    if process_this_frame:

        small_frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5).astype(np.uint8)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)       # Convert Image from BGR to RGB

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        # # Loop through the detected faces
        # for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #     matches = face_recognition.compare_faces(known_encodings, face_encoding)
        #     print(matches)
        # # faceDist = face_recognition.face_distance(known_encodings, face_encoding)

        #     name = "Unknown"
        #     face_distance = face_recognition.face_distance(known_encodings, face_encoding)
        #     print(face_distance)
        #     best_match_index = np.argmin(face_distance)
        #     if matches[best_match_index]:
        #     n ame = known_names[best_match_index]

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            print(face_distances)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index] and face_distances[best_match_index] <= 0.5:
                name = known_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        # Draw a box around the face and label it
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(frame, f"FPS: {str(fps)}", (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
