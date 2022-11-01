from os import path, getcwd, mkdir
from os.path import join, exists
from glob import glob
from cv2 import imwrite
EXTENSION_FILES = ["png", "jpeg", "jpg"]

class RecongnizedFacesService():

    def __init__(self):
        self.current_dir = getcwd()
        self.registred_faces_dir = join(self.current_dir + "\\data\\registred_faces")
        self.createRecognizedFacesDir()
        self.__list_of_files = []
        self.__list_of_names = []

    def getNamesFromFaces(self):
        return self.__list_of_names

    def getAuthorizedFaces(self):
        return self.__list_of_files

    def loadAutorizedFaces(self):
        for ext in EXTENSION_FILES:
            self.__list_of_files = [ f for f in glob( join(self.registred_faces_dir, f"*.{ext}") ) ]
        
        self.loadNameFromFaceFiles()

    def loadNameFromFaceFiles(self):
        for file in self.__list_of_files:
            name = ""
            for ext in EXTENSION_FILES:
                name = file.replace(self.registred_faces_dir, "").replace(f".{ext}", "")
            
            self.__list_of_names.append(name)

    def saveTakedPhoto(self, frame):
        name = input("Insira o nome de registro: ")
        imwrite(join(self.registred_faces_dir, name + ".jpg"), frame)

    def createRecognizedFacesDir(self):
        if not exists(self.registred_faces_dir):
            mkdir(self.current_dir + "\\data")
            mkdir(self.registred_faces_dir)