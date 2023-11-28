import socket as sck

#Costanti
SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096

def main():
    #Creazione dell'socket client
    client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    #Connessione al server
    client.connect(SERVER_ADDRESS)

    while True:

        nome_fiume = input("Specificare il nome del fiume: ")
        localita = input("Specificare la località del fiume: ")
        livello = input("Specificare il livello del fiume: ")
        file = input("Inserire il nome del file : ")
        
        client.sendall(f"{file}/{nome_fiume}/{localita}/{livello}".encode())
        
        message = client.recv(BUFSIZE).decode()
    
        print("\n\n" + message + "\n\n\n")
        
    client.close()
        



if __name__ == "__main__":
    main()