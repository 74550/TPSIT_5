#Librerie necessarie per il funzionamento del programma
import socket as sck

#Costanti
SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096
MENU = "1 - nome file presente\n2 -  numero di frammenti di un file a partire dal suo nome file\n3 - l’IP dell’host che ospita un frammento a partire nome file e dal numero del frammento\n4 -  tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file\n\n\n"

def main():
    #Creazione dell'socket client
    client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    #Connessione al server
    client.connect(SERVER_ADDRESS)

    while True:
        print(MENU)

        scelta_menu = int(input("Specificare il numero dell'operazione scelta : "))
        file = input("Inserire il nome del file : ")

        #Caso di default
        n_frammento = -1

        #Caso speciale
        if scelta_menu == 3:
            n_frammento = int(input("Inserire il numero del frammento : "))
        
        client.sendall(f"{file}/{scelta_menu}/{n_frammento}".encode())
        
        message = client.recv(BUFSIZE).decode()
    
        print("\n\n" + message + "\n\n\n")

    client.close()

if __name__ == "__main__":
    main()