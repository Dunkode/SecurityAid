from requests import request
from enviromentVariablesService import EnviromentVariablesService
import pickle

envVarServ = EnviromentVariablesService()

class TelegramLogger():

    def __init__(self):
        self.__bot_id = envVarServ.getTokenTelegramBot()
        self.__api_url = f"https://api.telegram.org/bot{self.__bot_id}/"
        self.__last_update_id = envVarServ.getLastUpdateId()
        self.__users_id = self.loadUsersIDs()

    #CONSULTAS NA API

    #Envio da foto
    def sendPhoto(self, chat_id, file_opened):
        method = "sendPhoto"
        params = {'chat_id': chat_id, "caption": "este é um teste"}
        files = {'photo': file_opened}
        resp = request("POST", self.__api_url + method, params, files=files)
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


    #CONTROLES

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
                            
                            envVarServ.addNewUser(new_user)
                
            except Exception as erro:
                print(f"Erro ao buscar novos usuários:{erro.args}")
        else:
            print("ATENÇÃO!\nO bot de monitoramento não está devidamente configurado!\nRevise suas configurações.")

        return envVarServ.getUsersId()
