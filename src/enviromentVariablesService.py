from os.path import join, exists
from os import getcwd, mkdir
import pickle

#Classe responsavel por gerenciar o arquivo de variaveis do ambiente
#como o Token para o BOT do Telegram e os usuarios que podem
#receber os alertas
class EnviromentVariablesService():
    def __init__(self):
        self.__variables = None
        self.__file_path = join(getcwd(), join("config", "env_var.dat"))
        self.loadEnviromentFile()

    #Le os dados do arquivo de variaveis e carrega na variavel
    def loadEnviromentFile(self):          
        dict = self.readFile()

        if dict == {}:
            dict = {"TELEGRAM_BOT_KEY" : "", "users" : [], "last_update_id" : ""}
            self.writeInFile(dict)
        
        self.__variables = dict

    #Salva os dados da variavel no arquivo e o carrega novamente
    def saveDataAndLoad(self):
        self.writeInFile(self.__variables)
        self.loadEnviromentFile()

    #Adiciona um novo usuario no arquivo de variaveis
    def addNewUser(self, new_user):      
        self.__variables["users"].append(new_user)
        self.saveDataAndLoad()

    #Getter dos usuarios salvos no arquivo
    def getUsersId(self):
        if self.__variables != None:
            return self.__variables["users"]

    #Atualiza o campo do ultimo update_id no arquivo de variaveis
    def updateLastUpdateId(self, update_id):
        self.__variables["last_update_id"] = update_id
        self.saveDataAndLoad()

    #Getter do ultimo update_id
    def getLastUpdateId(self):
        if self.__variables != None:
            return self.__variables["last_update_id"]


    #Getter do Token do BOT
    def getTokenTelegramBot(self):
        if self.__variables != None:
            return self.__variables["TELEGRAM_BOT_KEY"]

    #Funcao para saber se o chat_id ja esta cadastrado
    def idExists(self, chat_id):
        for user in self.__variables["users"]:
            if chat_id == user["chatID"]:
                return True
        
        return False

    #Funcao para leitura do arquivo de variaveis
    def readFile(self):
        #Verifica se o arquivo existe, criando-o caso nao
        if not exists(self.__file_path):
            if not exists(join(getcwd(), "config")):
                mkdir(join(getcwd(), "config"))

            t = open(self.__file_path, "w")
            t.close()
            return dict()

        with open(self.__file_path, "rb") as f:
            return pickle.load(f)
    
    #Funcao para escrita no arquivo de variaveis
    def writeInFile(self, data):
        with open(self.__file_path, "wb") as f:
            pickle.dump(data, f)   
    
    #
    def defineTelegramBotKey(self, key):
        self.__variables["TELEGRAM_BOT_KEY"] = key
        self.saveDataAndLoad()