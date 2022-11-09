from requests import request
from datetime import datetime
from os.path import join, exists
from os import getcwd, mkdir, remove
from cv2 import imencode
import schedule
import pickle
from glob import glob
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

    #####CONSULTAS NA API#####
    #Envio da foto
    def sendPhoto(self, user, data):
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
    # def montText(self):
    #     str = "🛑 ATENÇÃO 🛑\nFoi detectado um acesso não autorizado."
    #     str = str + f"\nData do registro: {time}"
    #     str = str + f"\nCor de autenticação: 🟥 Vermelho\n\n"

class TelegramScheduler():
    def __init__(self) :
        self.__path = join(getcwd() + "\\data\\send_files_queue")
        
        if not exists(self.__path):
            self.createQueuePath()

        self.__telegramLogger = TelegramLogger()
        schedule.every(1).minutes.do(self.readQueue)
        schedule.every(1).minutes.do(self.__telegramLogger.loadUsersIDs)
    
    def createQueuePath(self):
        if not exists(join(getcwd() + "\\data")):
            mkdir(join(getcwd() + "\\data"))
        
        mkdir(self.__path)

    def readQueue(self):
        filesNames = self.loadFileNamesInQueue()

        for fileName in filesNames:
            if "unauthorized" in fileName:
                dict = {}
                
                with open(fileName, "rb") as f:
                    dict = pickle.load(f)
                
                for id in self.__telegramLogger.getUsersId():
                    self.__telegramLogger.sendPhoto(id, dict)
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