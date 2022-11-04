from requests import request
from enviromentVariablesService import EnviromentVariablesService
import json

envVarServ = EnviromentVariablesService()

class TelegramLogger():

    def __init__(self):
        self.__bot_id = envVarServ.getTokenTelegramBot()
        self.__api_url = f"https://api.telegram.org/bot{self.__bot_id}/"
        self.__users_id = self.loadUsersIDs()

    #CONSULTAS NA API
    def sendPhoto(self, chat_id, file_opened):
        method = "sendPhoto"
        params = {'chat_id': chat_id, "caption": "este é um teste"}
        files = {'photo': file_opened}
        resp = request("POST", self.__api_url + method, params, files=files)
        return resp

    def getNewUserId(self):
        method = "getUpdates"
        params = {"limit": "1", "allowed_updates": "message"}
        resp = request("POST", self.__api_url + method, params=params)
        return resp.json()

    #CONTROLES
    def loadUsersIDs(self):
        if self.__bot_id != None and self.__bot_id != "":
            resp = self.getNewUserId()
            try:
                if resp["ok"]:
                    result = resp["result"][0]
                    message = result["message"]
                    
                    if envVarServ.idExists(message["chat"]["id"]):
                    
                        chat_id = message["chat"]["id"]
                        username = message["from"]["username"]
                        update_id = result["update_id"]

                        new_user = {"userName": username, "chatID": chat_id, "updateID": update_id}
                        
                        envVarServ.updateUsers(new_user)
            
            except Exception as erro:
                print(f"Erro ao buscar novos usuários:{erro.args}")
        else:
            print("ATENÇÃO!\nO bot de monitoramento não está devidamente configurado!\nRevise suas configurações.")
        return envVarServ.getUsersId()

    def getRegistredIDs(self):
        return self.__users_id
            

if __name__ == "__main__":
    pass
    telegram = TelegramLogger()
    print(telegram.getRegistredIDs())
