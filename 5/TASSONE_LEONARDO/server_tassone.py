#Librerie necessarie per il funzionamento del programma
import socket as sck
from threading import Thread
import sqlite3 as sql

#Costanti
SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096

#Lista di tutte le connessioni client
clients_list = []

class Client(Thread):
    """
    La classe client serve per gestire le operazione del client
    """
    def __init__(self, connection : sck.socket, address_client):
        Thread.__init__(self)
        self.connection = connection
        self.address_client = address_client

    def run(self):
        """
        Si richiede al client quale interrogazione desidera svolgere sul db\n
        Si interroga il db\n
        Si restituiscono i risultati
        """
        print("Esecuzione run")
        while True:
            message = self.connection.recv(BUFSIZE).decode()
            print("Messaggio arrivato")

            file_name, nome_fiume, localita, livello = message.split("/")[0], message.split("/")[1], message.split("/")[2], float(message.split("/")[3])
            self.db_interrogation(file_name, nome_fiume, localita, livello)
    
    def db_interrogation(self, file_name, nome_fiume, localita, livello):
        """
        Metodo per interrogare il db
        """
        #Connessione al db, interrogazione e ricezione dei dati
        connection_db = sql.connect("fiumi.db")
        cursor_db = connection_db.cursor()
        research = cursor_db.execute(f'SELECT livello FROM livelli WHERE fiume = "{nome_fiume}" AND localita = "{localita}"')
        research =research.fetchall()[0][0]
        stringa=b""
        

        if int((livello/research)*100) < 30:
            stringa=b"avvenuta ricezione"
        elif int((livello/research)*100) >= 30 and int((livello/research)*100) < 70:
            stringa=b"avvenuta ricezione"
            print("pericolo imminente")
        else:
            stringa=b"attivare sirena luminosa"
            print("PERICOLO!")

        research=str(research)
        if len(research) == 0:
            self.connection.sendall(b"La ricerca non restituisce risultati")
        else:
            print("invio risultati")
            self.connection.sendall(f"{stringa}")
        
        #Chiusura della connessione
        cursor_db.close()
        connection_db.close()

def main():
    #Creazione dell'socket server
    server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    
    #Associa al socket server l'indirizzo ip e porta
    server.bind(SERVER_ADDRESS)

    #Abilita il server a ricevere connessioni
    server.listen()

    while True:
        connection, address_client = server.accept()
        #Creazione thread e avvio
        client = Client(connection, address_client)
        client.start()
        #Inserimento nella lista per facilitarne la chiusura
        clients_list.append(client)
        print("client aggiunto")
    
    #Chisura dei thread e del socket
    for client in clients_list:
        client.join()
    server.close()

if __name__ == "__main__":
    main()