import math
import socket as sck
from threading import Thread
import random
import sqlite3

address = ('127.0.0.1',8000)

s_server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s_server.bind(address)

s_server.listen()


class Server(Thread):
    def __init__(self,c):
        Thread.__init__(self)
        self.conn = c

    def run(self):
            
            while 1:
                text = self.conn.recv(4096)
                testo = text.decode()
                list = testo.split(';') 
                conSQL = sqlite3.connect("file.db")
                cur = conSQL.cursor()
                list[1] = "'" + list[1] + "'"
    
                if list[0] == "1":
                    research = cur.execute(f"SELECT nome FROM files WHERE nome = {list[1]}")
                    db_lista = research.fetchall()[0][0]
                    if len(db_lista) > 0:
                        print(f"file {list[1]} presente")
                if list[0] == "2":
                    research = cur.execute(f"SELECT sum(frammenti.n_frammento) FROM files, frammenti WHERE files.id_file = frammenti.id_file AND files.nome = {list[1]}'")
                    db_lista = research.fetchall()[0][0]
                    if len(db_lista) > 0:
                        print(f"numero frammenti nel file {list[1]} = {db_lista}")
                if list[0] == "3":
                    research = cur.execute(f"SELECT frammenti.host FROM frammenti, files WHERE frammenti.id_file = files.id_file AND files.nome = {list[1]} AND frammenti.n_frammento = {list[2]}")
                    db_lista = research.fetchall()[0][0]
                    if len(db_lista) > 0:
                        print(f"indirizzo ip del file {list[1]} con frfammento numero: = {db_lista}")
                if list[0] == "4":
                    research = cur.execute(f"SELECT frammenti.host FROM frammenti, files WHERE frammenti.id_file = files.id_file AND files.nome = {list[1]}")
                    db_lista = research.fetchall()
                    if len(db_lista) > 0:
                        print(f"indirizzi ip di tutti i frammenti del file : {list[1]} = {db_lista}")
                 
                 
                

def main():

    while True:
        conn, add= s_server.accept()
        server = Server(conn)
        server.start()


        
            
if __name__ == "__main__":
    main()
    