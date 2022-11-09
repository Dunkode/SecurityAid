from os import system
from time import sleep
import numpy

from src.cameraManagerService import CameraManagerService
from src.enviromentVariablesService import EnviromentVariablesService
from src.recognizedFacesService import RecongnizedFacesService
from src.recognizerService import RecognizerService
from src.telegramLogger import TelegramLogger
from src.telegramLogger import TelegramScheduler

recognizedFacesServ = RecongnizedFacesService()
camService = CameraManagerService()
recognizerService = RecognizerService()
telegramLogger = TelegramLogger()
telegramScheduler = TelegramScheduler()

while True:
    # system('cls')

    print("{:-^40}".format("SecurityAid"))

    print('''
[1] Cadastrar rosto
[2] Iniciar monitoramento
[3] Configurar monitoramento
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

                        telegramScheduler.runScheduledTask()
                        
                        #Se tem faces localizadas
                        if recognizerService.getFaceLocations() != []:
    
                            #Desenha o identificador no rosto identificado
                            camService.drawIdenficationOnFrame(recognizerService.getFaceLocations(), recognizerService.getFaceNames())
                            
                            #Analisa a cor do crachá que a pessoa esta usando
                            camService.analiseTagColor(recognizerService.getFaceLocations())

                            if recognizerService.haveUnauthorizedPeoples():
                                telegramScheduler.createAlertUnauthorizedFile(camService.frame)
                            
                            
                        camService.showFrame("Monitoring...")

            case 3:
                inputStr = str(input("Escreva, por extenso, as cores que serão autorizadas neste ponto\nseparando-as por virgula." + 
                                    "\nCores disponíveis: \n\t→ AZUL\n\t→ VERMELHO\n\t→ VERDE\n\t→ AMARELO" + 
                                    "\n>> "))
                separetedColors = inputStr.lower().strip(" ").split(",")
                print(separetedColors)
            
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