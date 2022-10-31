from os import system
from time import sleep
from src.cameraManagerService import CameraManagerService
from src.recognizedFacesService import RecongnizedFacesService

recognizedFacesServ = RecongnizedFacesService()
camService = CameraManagerService()

while True:
    system('cls')

    print("{:-^40}".format("SecurityAid"))

    print('''
[1] Cadastrar rosto
[2] Iniciar monitoramento
[0] Fechar aplicativo
    ''')
    
    try:
        choice = int(input(">> "))

        match choice:
            case 0:
                quit()

            case 1:
                while True:
                    img = camService.takePhoto()
                    if img != None:
                        camService.closeCamera()
                        recognizedFacesServ.saveTakedPhoto(img)                        
                        print("Nova face registrada com sucesso!")
                        break
            case 2:
                print(recognizedFacesServ.getAuthorizedFaces())
                pass
            
                # while True:
                #     if camService.startCamera():
                #         camService.closeCamera()
                #         break
        sleep(3)
        
    except ValueError:
        print("Digite uma opção válida!")