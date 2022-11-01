import json

class EnviromentVariablesService():
    def __init__(self):
        self.__variables = None
        with open("config/auth.json") as f:
            self.__variables = json.load(f)

    def getTokenTelegramBot(self):
        if self.__variables != None:
            return self.__variables["TELEGRAM_BOT_KEY"]