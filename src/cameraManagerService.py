import cv2 as cv

class CameraManagerService():

    def __init__(self):
        self.frame = []
        self.frame_small = []
        self.__connectCamera = True

    def initializeCamera(self):
        if self.__connectCamera:
            self.__camera = cv.VideoCapture(0, cv.CAP_DSHOW)

        self.frame = self.__camera.read()[1]
        self.frame_small = cv.resize(self.frame, (0,0), fx=0.25, fy=0.25)
        self.__connectCamera = False

    def showFrame(self, windowName):
        cv.imshow(windowName, self.frame)
    
    def needCloseByEsc(self):
        k = cv.waitKey(60)
        return k == 27

    def takePhoto(self):
        self.initializeCamera()
        self.showFrame("Press (s) to registre a photo")
        k = cv.waitKey(60)
        return self.frame if k == ord('s') else False
    
    def closeCamera(self):
        self.__camera.release()        
        cv.destroyAllWindows()
        self.__connectCamera = True

    def drawIdenficationOnFrame(self, captured_face_locations, captured_face_name):
        for (top, right, bottom, left), name in zip(captured_face_locations, captured_face_name):
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