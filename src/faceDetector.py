import os
import face_recognition
import glob
import cv2 as cv
import numpy as np

EXTENSION_IMAGE = "png"

current_dir = os.getcwd()
path = os.path.join(current_dir, "faces\\")

list_of_files = [ f for f in glob.glob(path + f"*.{EXTENSION_IMAGE}") ]

print(f"Arquivos: {list_of_files}")


number_files = len(list_of_files)
names = list_of_files[:]

faces_encondings_database = []
faces_names_database = []

for i in range(number_files):
    presets = face_recognition.load_image_file(list_of_files[i])
    enconding = face_recognition.face_encodings(presets)[0]
    faces_encondings_database.append(enconding)
    nome = names[i].replace(current_dir + "\\faces\\", "").replace(f".{EXTENSION_IMAGE}", "")
    names[i] = nome
    faces_names_database.append(names[i])


face_locations = []
face_encondings_camera = []

camera = cv.VideoCapture(0, cv.CAP_DSHOW)

while True:
    frame = camera.read()[1]
    frame_small = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(frame_small)
    face_encondings_camera = face_recognition.face_encodings(frame_small, face_locations)
    face_names_camera = []
    
    for face_encoding in face_encondings_camera:
        print(face_encoding)
        matches = face_recognition.compare_faces(face_encondings_camera, face_encoding)
        name = "Desconhecido"
        face_distances = face_recognition.face_distance(faces_encondings_database, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = faces_names_database[best_match_index]
        
        face_names_camera.append(name)        

    #process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names_camera):
        top = int(top*4)
        right = int(right*4)
        bottom = int(bottom * 4)
        left = int(left * 4)
        # Draw a rectangle around the face
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Input text label with a name below the face
        cv.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6),
                    font, 0.5, (255, 255, 255), 1)
        
        # Display the resulting image
        cv.imshow('Video', frame)
    
    cv.imshow("frame_small", frame_small)


    k = cv.waitKey(60)
    if k == 27:
        break

camera.release()
cv.destroyAllWindows()
