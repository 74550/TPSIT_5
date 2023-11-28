#Librerie necessarie per il funzionamento del programma
import socket as sck
from threading import Thread
import sqlite3 as sql

#Costanti
SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096

#Lista di tutte le connessioni client
clients_list = []

#Dizionario di query possibili
query_dictionary = {1 : f"SELECT files.nome FROM files WHERE files.nome LIKE '?'", 
                    2 : f"SELECT files.tot_frammenti FROM files WHERE files.nome = '?'", 
                    3 : f"SELECT frammenti.host FROM frammenti, files WHERE frammenti.id_file = files.id_file AND files.nome = '?' AND n_frammento = !", 
                    4 : f"SELECT frammenti.host FROM frammenti, files WHERE frammenti.id_file = files.id_file AND files.nome = '?'"}

class Client(Thread):
    """
    La classe client serve per gestire le operazione del client
    """
    def __init__(self, connection : sck.socket, address_client):
        Thread.__init__(self)
        self.connection = connection
        self.address_client = address_client
        
        #dizionario delle risposte da inviare a seconda dell'interrogazione scelta
        self.send_answer_dictionary = {1 : self.send_answers_scelta_1,
                                       2 : self.send_answers_scelta_2,
                                       3 : self.send_answers_scelta_3,
                                       4 : self.send_answers_scelta_4}

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

            file_name, numero_scelta, n_frammento = message.split("/")[0], int(message.split("/")[1]), message.split("/")[2]

            if numero_scelta not in query_dictionary.keys():
                self.connection.sendall(b"Il numero del menu inserito non e' valido")
            else:
                self.db_interrogation(file_name, numero_scelta, n_frammento)
    
    def db_interrogation(self, file_name, numero_scelta, n_frammento):
        """
        Metodo per interrogare il db
        """
        #Si sostituiscono nel messaggio standard i dati inviati dal client
        messaggio_query = query_dictionary[numero_scelta]
        _messaggio_query = messaggio_query.replace("?", file_name)
        query = _messaggio_query

        #Caso particolare
        if numero_scelta == 3:
            __messaggio_query = _messaggio_query.replace("!", n_frammento)
            query = __messaggio_query
        
        #Connessione al db, interrogazione e ricezione dei dati
        connection_db = sql.connect("file.db")
        cursor_db = connection_db.cursor()
        res_db = cursor_db.execute(query)
        risultati = res_db.fetchall()

        if len(risultati) == 0:
            self.connection.sendall(b"La ricerca non restituisce risultati")
        else:
            print("invio risultati")
            self.send_answer_dictionary[numero_scelta](risultati)
        
        #Chiusura della connessione
        cursor_db.close()
        connection_db.close()
    
    def send_answers_scelta_1(self, risultati):
        """
        Metodo per inviare i risultati relativi alla prima opzione di interrogazione
        """
        self.connection.sendall(f"Il file ricercato {risultati[0][0]} e' presente nel database".encode())    
    
    def send_answers_scelta_2(self, risultati):
        """
        Metodo per inviare i risultati relativi alla seconda opzione di interrogazione
        """
        self.connection.sendall(f"{risultati[0][0]}".encode())
    
    def send_answers_scelta_3(self, risultati):
        """
        Metodo per inviare i risultati relativi alla terza opzione di interrogazione
        """
        self.connection.sendall(f"{risultati[0][0]}".encode())
    
    def send_answers_scelta_4(self, risultati):
        """
        Metodo per inviare i risultati relativi alla quarta opzione di interrogazione
        """
        stringa_risultato = ""
        for tupla in risultati:
            stringa_risultato += tupla[0] + "\n"
        self.connection.sendall(stringa_risultato.encode())
        
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