import sqlite3
import socket as sck
import time
from threading import Thread

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

def cercaNome(nome):
    con=sqlite3.connect("file.db")
    cur=con.cursor()
    res=cur.execute(f"SELECT nome FROM files WHERE nome='{nome}'")
    lista=res.fetchall()
    stringa= f"{lista[0][0]}"
    con.close()
    return(stringa)

class ThreadMess(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self,nome):
        while True:
            messaggio=f"{cercaNome(nome)}".encode()
            conn.sendall(messaggio)
            time.sleep(2)


def main():
    # bind
    address = ('0.0.0.0', 5000)
    s.bind(address)
    s.listen()

    connesione, clientAddress = s.accept()
    

    while True:
        tmess =ThreadMess(connesione)
        mex = connesione.recv(4096).decode() # mex decodificato in ascii 
        message=f"{cercaNome(mex)}".encode()
        tmess.start(message)
        connesione.close()
        s.close()


if __name__ == '__main__':
    main()




    
    