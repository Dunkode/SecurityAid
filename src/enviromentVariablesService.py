from os.path import join
from os import getcwd
import json

class EnviromentVariablesService():
    def __init__(self):
        self.__variables = None
        self.__file_path = join(getcwd(), join("config", "env_var.json"))
        self.loadEnviromentFile()

    def loadEnviromentFile(self):
        f = open(self.__file_path)    
        dict = json.load(f)
        if dict == {}:
            dict = {"TELEGRAM_BOT_KEY" : "", "users" : []}
            json.dump(dict, f)       
        
        f.close()
        self.__variables = dict

    def updateUsers(self, new_user):
        f = open(self.__file_path)        
        try:
            dict = json.load(f)
            f.close()
            
            dict["users"].append(new_user)
            f = open(self.__file_path, "w")
            json.dump(dict, f)
        finally:
            f.close()        
            self.loadEnviromentFile()


    def getTokenTelegramBot(self):
        if self.__variables != None:
            return self.__variables["TELEGRAM_BOT_KEY"]

    def getUsersId(self):
        if self.__variables != None:
            return self.__variables["users"]

    def idExists(self, chat_id):
        for user in self.__variables["users"]:
            if chat_id == user["chatID"]:
                return True
        
        return False