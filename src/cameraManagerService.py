import cv2 as cv

class CameraManagerService():

    def __init__(self):
        self.__camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.frame = []
        self.frame_small = []

    def initializeCamera(self, windowName):
        self.frame = self.__camera.read()[1]
        self.frame_small = cv.resize(self.frame, (0,0), fx=0.25, fy=0.25)
        cv.imshow(windowName, self.frame_small)

    def startCamera(self, windowName):
        self.initializeCamera(windowName)
        k = cv.waitKey(60)
        return k == 27

    def takePhoto(self):
        self.initializeCamera("Press (S) to registre a photo")
        k = cv.waitKey(60)
        return self.frame if k == ord('s') else None
    
    def closeCamera(self):
        self.__camera.release()        
        cv.destroyAllWindows()

    def drawIdenficationOnFrame(self, captured_face_locations, captured_faces_names):
        for (top, right, bottom, left), name in zip(captured_face_locations, captured_faces_names):
            top = int(top*4)
            right = int(right*4)
            bottom = int(bottom * 4)
            left = int(left * 4)

            # Draw a rectangle around the face
            cv.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Input text label with a name below the face
            cv.rectangle(self.frame, (left, bottom - 35),
                        (right, bottom), (0, 0, 255), cv.FILLED)

            font = cv.FONT_HERSHEY_DUPLEX
            cv.putText(self.frame, name, (left + 6, bottom - 6),
                        font, 0.5, (255, 255, 255), 1)