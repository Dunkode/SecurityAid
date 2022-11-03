from requests import request
from enviromentVariablesService import EnviromentVariablesService
from os.path import exists
import json

envVarServ = EnviromentVariablesService()

class TelegramLogger():

    def __init__(self):
        self.__bot_id = envVarServ.getTokenTelegramBot()
        self.__api_url = f"https://api.telegram.org/bot{self.__bot_id}/"
        self._registred_ids = self.loadRegistredIds() 

def sendPhoto(self, chat_id, file_opened):
    method = "sendPhoto"
    params = {'chat_id': chat_id, "caption": "este é um teste"}
    files = {'photo': file_opened}
    resp = request("POST", self.__api_url + method, params, files=files)
    return resp

def getUsersId(self):
    method = "getUpdates"
    params = {"limit": "1", "offset": self.__last_update_id, "allowed_updates": "message"}
    resp = request("POST", self.__api_url + method, params=params)
    

    return resp.json()

def loadResgistredIds(self):
    if not exists("data/registred_ids.json"):
        with open("data/registred_ids.json", "w") as f:
            f.write(dict())
        
    return json.open("data/registred_ids.json")


if __name__ == "__main__":
    telegram = TelegramLogger()
    print(telegram.getUsersId())
