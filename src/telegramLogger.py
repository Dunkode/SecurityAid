from requests import request
from src.enviromentVariablesService import EnviromentVariablesService

envVarServ = EnviromentVariablesService()

class TelegramLogger():

    def __init__(self):
        self.__bot_id = envVarServ.getTokenTelegramBot()
        self.__api_url = f"https://api.telegram.org/bot{self.__bot_id}/"
        self.__last_update_id = 0 

def send_photo(self, chat_id, file_opened):
    method = "sendPhoto"
    params = {'chat_id': chat_id, "caption": "este é um teste"}
    files = {'photo': file_opened}
    resp = request("POST", self.__api_url + method, params, files=files)
    return resp

def get_user_id(self):
    method = "getUpdates"
    params = {"limit": "1", "offset": self.__last_update_id, "allowed_updates": "message"}
    resp = request("POST", self.__api_url + method, params=params)

    return resp.json()