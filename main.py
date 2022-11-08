from os import system
from time import sleep
import numpy

from src.cameraManagerService import CameraManagerService
from src.enviromentVariablesService import EnviromentVariablesService
from src.recognizedFacesService import RecongnizedFacesService
from src.recognizerService import RecognizerService
from src.telegramLogger import TelegramLogger

recognizedFacesServ = RecongnizedFacesService()
camService = CameraManagerService()
recognizerService = RecognizerService()
telegramLogger = TelegramLogger()

while True:
    # system('cls')

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

                    if isinstance(img, numpy.ndarray):
                        camService.closeCamera()
                        recognizedFacesServ.saveTakedPhoto(img)                        
                        print("Nova face registrada com sucesso!")
                        break
                    
            case 2:
                #Carrega as fotos da pessoas autorizadas
                recognizedFacesServ.loadAutorizedFaces()
                #Carrega os nomes atrelados a essas fotos
                recognizedFacesServ.loadNameFromFaceFiles()

                #Realiza um reconhecimento do encoding de cada foto salva
                recognizerService.recognizeRegistredFaces(recognizedFacesServ.getNamesFromFaces(), recognizedFacesServ.getAuthorizedFaces())

                while True:
                    camService.initializeCamera()

                    if camService.needCloseByEsc():
                        #Fecha a camera
                        camService.closeCamera()
                        break
                    else:
                        #Reconhece as faces captadas na camera
                        recognizerService.recognizeFacesFromFrame(camService.frame_small)

                        #Se tem faces localizadas
                        if recognizerService.getFaceLocations() != []:
    
                        #Desenha o identificador no rosto identificado
                            camService.drawIdenficationOnFrame(recognizerService.getFaceLocations(), recognizerService.getFaceNames())
                            
                            print(camService.analiseTagColor(recognizerService.getFaceLocations()))

                        #     if recognizerService.haveUnauthorizedPeoples():
                        #         telegramLogger.getNewUserId()
                        #         pass
                        # #Mostra o frame desenhado
                        camService.showFrame("Monitoring...")
                        
            #FUNCAO SECRETA
            case 999:
                envVarService = EnviromentVariablesService()
                key = str(input("Insira a Chave do BOT >> "))
                envVarService.defineTelegramBotKey(key)
                print("BOT cadastrado com sucesso!")

        sleep(3)
        
    except ValueError:
        print("Digite uma opção válida!")

    except Exception as erro:
        print(erro.args)