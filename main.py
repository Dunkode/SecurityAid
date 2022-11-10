from time import sleep
from os import system
import numpy

from src.enviromentVariablesService import EnviromentVariablesService
from src.recognizedFacesService import RecongnizedFacesService
from src.cameraManagerService import CameraManagerService
from src.recognizerService import RecognizerService
from src.telegramService import TelegramScheduler
from src.telegramService import TelegramLogger

recognizedFacesServ = RecongnizedFacesService()
envVarService = EnviromentVariablesService()
recognizerService = RecognizerService()
telegramScheduler = TelegramScheduler()
camService = CameraManagerService()
telegramLogger = TelegramLogger()

while True:
    system('cls')

    print("{:-^40}".format("SecurityAid"))

    print('''
[1] Cadastrar rosto
[2] Iniciar monitoramento
[3] Configurar cores do monitoramento
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
                
                #Se tem fotos de pessoas autorizadas
                if len(recognizedFacesServ.getAuthorizedFaces()) > 0:
                   
                    #Realiza um reconhecimento do encoding de cada foto salva
                    recognizerService.recognizeRegistredFaces(recognizedFacesServ.getNamesFromFaces(), recognizedFacesServ.getAuthorizedFaces())

                    #Pega as cores autorizadas do setor
                    colorsAuthorized = envVarService.getAuthorizedColors()
                    colorIdentified = None

                    while True:
                        #Inicializa a camera
                        camService.initializeCamera()
                        
                        if camService.needCloseByEsc():
                            #Fecha a camera
                            camService.closeCamera()
                            break
                        
                        else:
                            #Reconhece as faces captadas na camera
                            recognizerService.recognizeFacesFromFrame(camService.frame_small)

                            #Verifica se precisa rodar o envio de mensagens ou
                            #o cadastro de novos usuarios
                            telegramScheduler.runScheduledTask()
                            
                            #Se tem faces localizadas e faces autorizadas
                            if len(recognizerService.getFaceLocations()) > 0:
        
                                #Desenha o identificador no rosto identificado
                                camService.drawIdenficationOnFrame(recognizerService.getFaceLocations(), recognizerService.getFaceNames())
                                
                                #Para cada face identificada
                                for face_location in recognizerService.getFaceLocations():
                                    #Analisa a cor do crachá que a pessoa esta usando
                                    colorIdentified = camService.analiseTagColor(face_location)
                                    
                                    #Se a cor do cracha da pessoa identificada nao pode ser usada
                                    #no setor atual
                                    if colorIdentified != None and colorIdentified not in colorsAuthorized:
                                        name = recognizerService.getNameByFaceLocation(face_location)
                                        telegramScheduler.createAlertUnauthorizedColorFile(camService.frame, name, colorIdentified)


                                #Se tem pessoas nao autorizadas no setor
                                if recognizerService.haveUnauthorizedPeoples():
                                    telegramScheduler.createAlertUnauthorizedFile(camService.frame)
                                
                        camService.showFrame("Monitoring...")
                else:
                    print("Cadastre rostos para poder realizar o monitoramento!")

            case 3:
                inputStr = str(input("Escreva, por extenso, as cores que serão autorizadas neste ponto\nseparando-as por virgula." + 
                                    "\nCores disponíveis: \n\t→ AZUL\n\t→ VERMELHO\n\t→ VERDE\n\t→ AMARELO" + 
                                    "\n>> "))
                
                separetedColors = inputStr.upper().strip(" ").split(",")

                envVarService.saveAuthorizedColors(separetedColors)            
            
            #FUNCAO SECRETA
            #Cadastro do Token do BOT
            case 999:
                key = str(input("Insira a Chave do BOT >> "))
                envVarService.defineTelegramBotKey(key)
                print("BOT cadastrado com sucesso!")

        sleep(3)
        
    except ValueError:
        print("Digite uma opção válida!")

    except Exception as erro:
        print(erro.args)