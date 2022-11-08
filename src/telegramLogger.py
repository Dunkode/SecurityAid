from requests import request
from src.enviromentVariablesService import EnviromentVariablesService
from datetime import datetime

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
    def sendPhoto(self, chat_id, file_opened):
        method = "sendPhoto"
        params = {'chat_id': chat_id, "caption": self.montText()}
        files = {'photo': file_opened}
        resp = request("POST", self.__api_url + method, params=params, files=files)
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

    def montText(self):
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        str = "🛑 ATENÇÃO 🛑\nFoi detectado um acesso não autorizado."
        str = str + f"\nData do registro: {time}"
        str = str + f"\nCor de autenticação: 🟥 Vermelho\n\n"