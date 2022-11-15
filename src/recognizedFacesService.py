from os.path import join, exists
from os import getcwd, mkdir, remove
from cv2 import imwrite
from glob import glob

EXTENSION_FILES = ["png", "jpeg", "jpg"]

#Classe responsavel por carregar no sistema as fotos
#e nomes das pessoas autorizadas
class RecongnizedFacesService():

    def __init__(self):
        self.current_dir = getcwd()
        self.registred_faces_dir = join(self.current_dir,  join("data", "registred_faces"))
        self.createRecognizedFacesDir()
        self.__list_of_files = []
        self.__list_of_names = []

    def getNamesFromFaces(self):
        return self.__list_of_names

    def getAuthorizedFaces(self):
        return self.__list_of_files

    def loadAutorizedFaces(self):
        for ext in EXTENSION_FILES:
            for f in glob( join(self.registred_faces_dir, f"*.{ext}") ):
                self.__list_of_files.append(f)
        
        self.loadNameFromFaceFiles()

    def loadNameFromFaceFiles(self):
        for file in self.__list_of_files:
            name = ""
            for ext in EXTENSION_FILES:
                name = file.replace(self.registred_faces_dir, "").replace(f".{ext}", "").replace("\\", "")
            
            self.__list_of_names.append(name)

    def saveTakedPhoto(self, frame):
        name = input("Insira o nome de registro: ")
        imwrite(join(self.registred_faces_dir, name + ".jpg"), frame)
    
    def removeRegistredFace(self, name):
        index = self.__list_of_names.index(name)
        fileToRemove = self.__list_of_files[index]
        remove(fileToRemove)
        self.__list_of_names.pop(index)
        self.__list_of_files.pop(index)


    def createRecognizedFacesDir(self):
        if not exists(self.registred_faces_dir):
            if not exists(join(self.current_dir, "data")):
                mkdir(join(self.current_dir, "data"))
            
            mkdir(self.registred_faces_dir)