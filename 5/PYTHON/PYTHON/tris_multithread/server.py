from ast import While
from pickle import TRUE
from pydoc import cli
import socket as sck
from threading import Thread, Lock

SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096

lock = Lock()
turn = 1
id_client = 0
clients_list = []
game_status = {n : n for n in range(8)}

class Client(Thread):
    def __init__(self, connection : sck.socket, client_address):
        global id_client

        self.connection = connection
        self.client_address = client_address
        self.isRunning = True

        lock.acquire()
        self.id = id_client + 1
        id_client += 1
        lock.release()

        if self.id == 0:
            self.symbol = "X"
        else:
            self.symbol = "O"

    def run(self):
        global turn
        while True:
            while True:
                if self.id % 2 == 0 and turn % 2 == 0:
                    break
                elif self.id % 2 != 0 and turn % 2 != 0:
                    break

            while True:
                move = self.connection.recv(BUFSIZE).decode()
                if game_status[move] != move:
                    self.connection.sendall(b"Mossa gia' effettuata dall'avversario, inserirne un'altra")
                    continue
                break
            game_status[move] = self.symbol
            message_to_send = ""
            for key, statment in game_status.items():
                message_to_send += f"{statment}\t\t"
                if key == 2 or key == 5:
                    message_to_send += f"\n----------\n"
            self.connection.sendall(message_to_send.encode())
            turn += 1
            if turn == 9:
                self.isRunning = False
                break


def main():
    server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen()

    for _ in range(2):
        connection, client_address = server.accept()
        client = Client(connection, client_address)
        client.start()
        clients_list.append(client)

    while True:
        if clients_list[0].isRunning == False or clients_list[1].isRunning == False:
            break
    
    for client in clients_list:
        client.join()
    server.close()

if __name__ == "__main__":
    main()