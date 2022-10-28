from os import system
from time import sleep

from src.recognizedFacesService import RecongnizedFacesService

while True:
    system('cls')

    recognizedFacesServ = RecongnizedFacesService()

    print("{:-^40}".format("SecurityAid"))

    print('''
[1] Cadastrar rosto
[2] Iniciar monitoramento
[0] Fechar aplicativo
    ''')
    
    try:
        choice = int(input(">> "))

        match choice:
            case 0:
                quit()
            case 1:
                pass
            case 2:
                print(recognizedFacesServ.getAuthorizedFaces())
                pass
            
        sleep(3)
        
    except ValueError:
        print("Digite uma opção válida!")