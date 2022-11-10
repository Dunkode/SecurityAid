from os import getcwd, mkdir, remove
from os.path import join, exists
from datetime import datetime
from requests import request
from cv2 import imencode
from glob import glob
import schedule
import pickle
import io


from src.enviromentVariablesService import EnviromentVariablesService

envVarServ = EnviromentVariablesService()

#Classe responsavel por fazer o envio de mensagens de alerta
#de pessoas nao autorizadas, assim como o cadastro de novas
#pessoas que devem receber esses alertas
class TelegramLogger():

    def __init__(self):
        self.__bot_id = envVarServ.getTokenTelegramBot()
        self.__api_url = f"https://api.telegram.org/bot{self.__bot_id}/"
        self.__last_update_id = envVarServ.getLastUpdateId()
        self.__users_id = self.loadUsersIDs()

    #####API#####
    
    #Envio do alerta de pessoa nao autorizada
    def sendUnauthorizedAlertPhoto(self, user, data):
        #Escrita da imagem em buffer de memoria
        #para conseguir enviar ela pela API
        _, buffer = imencode(".jpg", data["img"])
        ioBuffer = io.BytesIO(buffer)

        method = "sendPhoto"
        params = {'chat_id': user["chatID"], "caption": self.montAlertUnauthorizedMessage(data["date"])}
        files = {'photo': ioBuffer}
        resp = request("POST", self.__api_url + method, params=params, files=files)
        ioBuffer.close()
        return resp
    
    #Envio do alerta de pessoa usando uma cor nao autorizada
    #naquele setor
    def sendUnauthorizedColorAlertPhoto(self, user, data):
        #Escrita da imagem em buffer de memoria
        #para conseguir enviar ela pela API
        _, buffer = imencode(".jpg", data["img"])
        ioBuffer = io.BytesIO(buffer)

        method = "sendPhoto"
        params = {'chat_id': user["chatID"], "caption": self.montAlertUnauthorizedColorMessage(data)}
        files = {'photo': ioBuffer}
        resp = request("POST", self.__api_url + method, params=params, files=files)
        ioBuffer.close()
        return resp
    
    #Envio de mensagem para confirmacao de cadastro na API
    def sendGreatingsMessage(self, chat_id):
        method = "sendMessage"
        params = {"chat_id": chat_id, "text": "✅ Seu usuário foi registrado com sucesso!\nVocê passará a receber alertas de acesso não autorizado."}
        resp = request("POST", self.__api_url + method, params=params)
        return resp

    #Consulta da última mensagem recebida pelo BOT
    def getNewUserId(self):
        method = "getUpdates"
        
        if self.__last_update_id != None and self.__last_update_id != "":
            params = {"limit" : "1", "offset" : self.__last_update_id+1, "allowed_updates" : ["message"]}
        
        else:
            params = {"limit": "1", "allowed_updates" : ["message"]}
        
        resp = request("POST", self.__api_url + method, params=params)
        return resp.json()


    #####CONTROLES#####
    #Funcao para controlar o carregamento dos usuarios cadastrados
    def loadUsersIDs(self):
        if self.__bot_id != None and self.__bot_id != "":
            resp = self.getNewUserId()
            try:
                if resp["ok"] and resp["result"] != []:
                        result = resp["result"][0]
                        message = result["message"]
                        
                        update_id = result["update_id"]
                        envVarServ.updateLastUpdateId(update_id)

                        if not envVarServ.idExists(message["chat"]["id"]) and message["text"] == "/start":
                            chat_id = message["chat"]["id"]
                            username = message["from"]["username"]

                            new_user = {"userName": username, "chatID": chat_id}
                            
                            self.sendGreatingsMessage(chat_id)
                            envVarServ.addNewUser(new_user)
                
            except Exception as erro:
                print(f"Erro ao buscar novos usuários:{erro.args}")
        else:
            print("ATENÇÃO!\nO bot de monitoramento não está devidamente configurado!\nRevise suas configurações.")

        return envVarServ.getUsersId()
    
    #Getter dos id's carregados
    def getUsersId(self):
        return self.__users_id

    def montAlertUnauthorizedMessage(self, time):
        str = "🛑 ATENÇÃO 🛑\nFoi detectado um acesso não autorizado."
        str = str + f"\nData do registro: {time}"
        return str
    
    def montAlertUnauthorizedColorMessage(self, data):
        str = "🛑 ATENÇÃO 🛑\nO usuário {} foi identificado em uma área não permitida.".format(data["name"])
        str = str + "\nData do registro: {}".format(data["date"])
        str = str + "\nCor do crachá: {}".format(self.selectColorMessage(data["color"]))
        return str

    def selectColorMessage(self, color):
        match color:
            case "AZUL":
                return "🟦 Azul"
            case "VERMELHO":
                return "🟥 Vermelho"
            case "VERDE":
                return "🟩 Verde"
            case "AMARELO":
                return "🟨 Amarelo"
    
class TelegramScheduler():
    def __init__(self) :
        self.__path = join(getcwd(), join("data", "send_files_queue"))
        
        if not exists(self.__path):
            self.createQueuePath()

        self.__telegramLogger = TelegramLogger()
        schedule.every(1).minutes.do(self.readQueue)
        schedule.every(1).minutes.do(self.__telegramLogger.loadUsersIDs)
    
    def createQueuePath(self):
        if not exists(join(getcwd(), "data")):
            mkdir(join(getcwd(), "data"))
        
        mkdir(self.__path)

    def readQueue(self):
        filesNames = self.loadFileNamesInQueue()

        for fileName in filesNames:
            dict = {}
                
            with open(fileName, "rb") as f:
                dict = pickle.load(f)

            for id in self.__telegramLogger.getUsersId():
                
                if "unauthorized_alert" in fileName:                
                    self.__telegramLogger.sendUnauthorizedAlertPhoto(id, dict)
                
                elif "unauthorized_color_alert" in fileName:
                    self.__telegramLogger.sendUnauthorizedColorAlertPhoto(id, dict)
                
            remove(fileName)


    def runScheduledTask(self):
        schedule.run_pending()

    def loadFileNamesInQueue(self):
        return [ f for f in glob( join(self.__path, "*.dat") ) ]
    
    def createAlertUnauthorizedFile(self, img):
        now = datetime.now()
        dict = {"date" : now.strftime("%d/%m/%Y %H:%M:%S"), "img" : img}
        timestr = now.strftime("%d%m%Y%H%M")
        
        with open(join(self.__path, f"unauthorized_alert_{timestr}.dat"), "wb") as f:
             pickle.dump(dict, f)
             
    def createAlertUnauthorizedColorFile(self, img, name, color):
        now = datetime.now()
        dict = {
            "date" : now.strftime("%d/%m/%Y %H:%M:%S"), 
            "img" : img, 
            "name" : name, 
            "color" : color
        }
        timestr = now.strftime("%d%m%Y%H%M")
        
        with open(join(self.__path, f"unauthorized_color_alert_{timestr}.dat"), "wb") as f:
             pickle.dump(dict, f)