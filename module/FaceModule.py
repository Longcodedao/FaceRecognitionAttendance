import cv2
import face_recognition
import numpy as np
import os

def FaceDetection(image):
    # Initail know_encodeings and know_names
    known_encodings = []
    known_names = []
    
    # Load images from the specified folders
    for folder in os.listdir(os.path.join(os.getcwd(), 'data', 'images')):
        print(os.listdir(folder))
        for file in os.listdir(folder):
            image_path = os.path.join(folder, file)
            known_img = face_recognition.load_image_file(image_path)
            known_encoding = face_recognition.face_encodings(known_img)[0]
            known_encodings.append(known_encoding)
            known_names.append(folder)
     
    # Initial img
    img = image
    
    #Resize image to small image
    resized_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5).astype(np.uint8)
    
    #Transfering BGR_image to RGB_image
    RGB_resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRB)
    
    #Find face location in img -> list
    face_locations = face_recognition.face_locations(RGB_resized_img)
    
    #Encoding face -> list
    face_encodings = face_recognition.face_encodings(RGB_resized_img, face_locations)
    
    # Create a file name to save name of face -> list
    face_names = []
    
    # Take each face_encoding in face_encodings because face_encodings is a list
    for face_encoding in face_encodings:
        
        # Compare current face to all -> list
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        
        name = 'Unknow'
        
        # Find distance from current face to each know face -> list
        face_distances = face_recognition.face_distance(face_encodings, face_encoding)
        
        # Return index at mininmun distance in face_distances
        best_match_index = np.argmin(face_distances)
        
        # Check distance
        if matches[best_match_index] and face_distances[best_match_index] <= 0.5:
            name = known_names[best_match_index]
            face_names.append(name)
        
        # Draw boudning box anh put name of face
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top = top * 2
            right = right * 2
            bottom = bottom * 2
            left = left * 2
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(img, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    return img
