import face_recognition
import numpy as np

class RecognizerService():

    def __init__(self):
        self.__registred_faces_encodings = []
        self.__registred_faces_names = []
        self.__captured_face_locations = []
        self.__captured_face_encondings = []
        self.__captured_faces_names = []

    def recognizeRegistredFaces(self, names, files):
        for i in range(len(files)):
            presets = face_recognition.load_image_file(files[i])
            enconding = face_recognition.face_encodings(presets)[0]
            self.__registred_faces_encodings.append(enconding)
            self.__registred_faces_names.append(names[i])
    
    def recognizeFacesFromFrame(self, frame_small):
        self.__captured_face_locations = face_recognition.face_locations(frame_small)
        self.__captured_face_encondings = face_recognition.face_encodings(frame_small, self.__captured_face_locations)

        for face_encoding in self.__captured_face_encondings:
            matches = face_recognition.compare_faces(self.__registred_faces_encodings, face_encoding)
            name = "Desconhecido"
            face_distances = face_recognition.face_distance(self.__registred_faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = self.__registred_faces_encodings[best_match_index]
            
            self.__captured_faces_names.append(name)

