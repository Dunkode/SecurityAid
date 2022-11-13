from time import sleep
from os import system
import numpy


from src.enviromentVariablesService import EnviromentVariablesService
from src.telegramService import TelegramScheduler
from src.telegramService import TelegramLogger
from src.recognizedFacesService import RecongnizedFacesService
from src.cameraManagerService import CameraManagerService
from src.consoleLoggerUtil import ConsoleLoggerUtil as log
from src.recognizerService import RecognizerService

envVarService = EnviromentVariablesService()
log.info("Inicializando serviço de controle de variáveis de ambiente.")

telegramScheduler = TelegramScheduler()
log.info("Inicializando agendador de envio de mensagens.")

telegramLogger = TelegramLogger()
log.info("Inicializando logger do Telegram.")

recognizedFacesServ = RecongnizedFacesService()
log.info("Inicializando serviço de reconhecimento de faces cadastradas.")

camService = CameraManagerService()
log.info("Inicializando serviço de gerenciamento de camera.")

recognizerService = RecognizerService()
log.info("Inicializando serviço de reconhecimento de faces.")

while True:
    sleep(2)
    system("cls")

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
                log.info("Encerrando o sistema.")
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

                    log.info("Iniciando monitoramento...")
                    
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
                                
                        camService.showFrame("Tela de monitoramento")
                else:
                    log.warning("Cadastre faces para iniciar o monitoramento!")
            case 3:
                #Lista com as cores que estao mapeadas no projeto
                possibleColors = ["AZUL", "VERMELHO", "VERDE", "AMARELO"]

                inputStr = str(input("Escreva, por extenso, as cores que serão autorizadas neste ponto\nseparando-as por virgula." + 
                                    "\nCores disponíveis: \n\t→ AZUL\n\t→ VERMELHO\n\t→ VERDE\n\t→ AMARELO" + 
                                    "\n>> "))
                
                separetedColors = inputStr.upper().replace(" ", "").split(",")

                salvar = True
                for color in separetedColors:
                    if color not in possibleColors:
                        log.warning(f"Foi inserida uma cor inválida:\'{color}\'\nInsira as cores novamente!")
                        salvar = False
                
                if salvar:
                    envVarService.saveAuthorizedColors(separetedColors)            
                    log.info("Cores cadastradas com sucesso!")            
            #FUNCAO SECRETA
            #Cadastro do Token do BOT
            case 999:
                key = str(input("Insira a Chave do BOT >> "))
                envVarService.defineTelegramBotKey(key)
                print("BOT cadastrado com sucesso!")
        
    except ValueError as ve:
        log.error("Digite uma opção válida!")
    except Exception as erro:
        log.error(f"Ocorreu um erro: {erro.args}")