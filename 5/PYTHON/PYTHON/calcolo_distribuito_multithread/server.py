import socket as sck
from threading import Thread, Lock
import sqlite3 as sql

SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096

lock = Lock()
id_clients = 0
operations = {} #{client_id : 'operation'}

class Client(Thread):
    def __init__(self, connection : sck.socket, client_address):
        global id_clients
        
        Thread.__init__(self)
        self.connection = connection
        self.client_address = client_address

        lock.acquire()
        self.id = id_clients + 1
        id_clients += 1
        lock.release()
    
    def run(self):
        global operations

        message_to_send = ""
        for client_id, operations_serie in operations.items():
            if client_id == self.id:
                for operation in operations_serie:
                    message_to_send += f"{operation};"

        self.connection.sendall(f"{message_to_send[:-1]}".encode())

        results = self.connection.recv(BUFSIZE).decode()
        results_list = results.split(";")

        for index, result in enumerate(results_list):
            print(f"{operations[self.id][index]} = {result} from {self.client_address[0]} - {self.client_address[1]}")
        print("\n\n\n")
        
        self.connection.sendall(b"exit")

def db_interrogation():
    global operations

    db_connection = sql.connect("operations.db")
    db_cursor = db_connection.cursor()
    
    db_res = db_cursor.execute("SELECT client, operation FROM operations")
    results = db_res.fetchall()

    db_cursor.close()
    db_connection.close()

    for tupla in results:
        client_id = tupla[0]
        operation = tupla[1]

        if client_id not in operations:
            operations[client_id] = [operation]
        else:
            operations[client_id].append(operation)

def main():
    db_interrogation()

    clients_list = []
    server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen()

    while True:
        connection, client_address = server.accept()
        client = Client(connection, client_address)
        client.start()
        clients_list.append(client)

    for client in clients_list:
        client.join()
    server.close()

if __name__ == "__main__":
    main()