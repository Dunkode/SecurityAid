import cv2 as cv
import numpy as np

from src.rangeColorsConst import RangeColorsConst

#Classe responsavel pelo gerenciamento da camera
#Como leitura em video, desenho das faces identificadas ou nao
#etc...
class CameraManagerService():

    def __init__(self):
        self.frame = []
        self.frame_small = []
        self.__connectCamera = True
        self.__COLOR_RECOGNIZED = (0,255,0)
        self.__COLOR_UNRECOGNIZED = (0,0,255)
        self.__font = cv.FONT_HERSHEY_DUPLEX
        self.__altura = 0
        self.__largura = 0

    def initializeCamera(self):
        if self.__connectCamera:
            self.__camera = cv.VideoCapture(0, cv.CAP_DSHOW)

        self.frame = self.__camera.read()[1]
        self.frame = cv.flip(self.frame, 1)
        self.frame_small = cv.resize(self.frame, (0,0), fx=0.25, fy=0.25)
        self.__connectCamera = False
        self.__altura, self.__largura, _ = np.shape(self.frame)

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
        cv.imwrite("teste.jpg", self.frame)
        self.__camera.release()        
        cv.destroyAllWindows()
        self.__connectCamera = True

    def drawIdenficationOnFrame(self, captured_face_locations, captured_face_name):
        for (top, right, bottom, left), name in zip(captured_face_locations, captured_face_name):
            isAuthorized = name != "UNAUTHORIZED"
            
            top = int(top*4)
            right = int(right*4)
            bottom = int(bottom * 4)
            left = int(left * 4)
            
            # Draw a rectangle around the face
            cv.rectangle(self.frame, 
                            (left, top), 
                            (right, bottom), 
                            self.__COLOR_RECOGNIZED if isAuthorized else self.__COLOR_UNRECOGNIZED , 
                            2)
            
            # Input text label with a name below the face
            cv.rectangle(self.frame, 
                            (left, bottom - 35),
                            (right, bottom), 
                            self.__COLOR_RECOGNIZED if isAuthorized else self.__COLOR_UNRECOGNIZED , 
                            cv.FILLED)

            cv.putText(self.frame, name, 
                        (left + 6, bottom - 6),
                        self.__font, 
                        0.5, 
                        (255, 255, 255), 
                        1)
            
               
    def analiseTagColor(self, captured_face_locations):
        rangeColor = RangeColorsConst()
        for (top, right, bottom, left) in captured_face_locations:
            percentColors = []

            top = (int(top * 4) + 200) if (int(top * 4) + 200) < self.__altura else self.__altura 
            right = int(right * 4)
            bottom = (int(bottom * 4) + 200) if (int(bottom * 4) + 200) < self.__altura else self.__altura
            left = int(left * 4)

            roi = self.frame[top : bottom , left : right]

            contorsBlue   = self.findContorsWithRangeColor(roi, rangeColor.LOWER_BLUE, rangeColor.UPPER_BLUE)
            contorsRed    = self.findContorsWithRangeColor(roi, rangeColor.LOWER_RED, rangeColor.UPPER_RED)
            contorsGreen  = self.findContorsWithRangeColor(roi, rangeColor.LOWER_GREEN, rangeColor.UPPER_GREEN)
            contorsYellow = self.findContorsWithRangeColor(roi, rangeColor.LOWER_YELLOW, rangeColor.UPPER_YELLOW)
            
            percentColors.append(self.calculatePercentageOfColor(roi, rangeColor.LOWER_BLUE, rangeColor.UPPER_BLUE, contorsBlue))
            percentColors.append(self.calculatePercentageOfColor(roi, rangeColor.LOWER_RED, rangeColor.UPPER_RED, contorsRed))
            percentColors.append(self.calculatePercentageOfColor(roi, rangeColor.LOWER_GREEN, rangeColor.UPPER_GREEN, contorsGreen))
            percentColors.append(self.calculatePercentageOfColor(roi, rangeColor.UPPER_YELLOW, rangeColor.UPPER_YELLOW, contorsYellow))

            predominantColor = max(percentColors)
            if predominantColor != 0:
                match percentColors.index(predominantColor):
                    case 0:
                        return "AZUL"
                    case 1:
                        return "VERMELHO"
                    case 2:
                        return "VERDE"
                    case 3:
                        return "AMARELO"

            return "SEM COR DE IDENTIFICAÇÃO"

            # Input text label with a name below the face
            # cv.rectangle(self.frame, 
            #                 (left, top), 
            #                 (right, bottom), 
            #                 self.__COLOR_RECOGNIZED,
            #                 2)

            # cv.imshow("roi", roi)
            # cv.imwrite("coisa.png", self.frame)
            # quit()

    def findContorsWithRangeColor(self, frame, lower, upper):
        hsv    =  cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask   =  cv.inRange(hsv, lower, upper)
        bit    =  cv.bitwise_and(frame, frame, mask=mask)
        gray   =  cv.cvtColor(bit, cv.COLOR_BGR2GRAY)
        border =  cv.threshold(gray, 3, 255, cv.THRESH_BINARY)[1]

        return cv.findContours(border, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

    def calculatePercentageOfColor(self, frame, lower, upper, contors):
        for contour in contors:
            area = cv.contourArea(contour)
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lower, upper)

            if area > 800:
                ratio = cv.countNonZero(mask) / (frame.size)
                return np.round(( ratio * 100 ), 2)     
        
        return 0.0