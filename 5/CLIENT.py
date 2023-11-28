from pickle import TRUE
import socket as sck
from threading import Thread

address = ('127.0.0.1',8000)

s_client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

class Client(Thread):
        def __init__(self, s = s_client):
            Thread.__init__(self)
            self.s_client = s
        def run(self):
            s_client.connect(address)

            while 1:
                print(s_client.recv(4096).decode())


def main():
    client = Client()
    client.start()
    while 1:
        mex = input("1 VERIFICA PRESENZA FILE\n2 NUMERO FRAMMENTI DATO UN FILE\n3 DATO NUME FILE E NUMERO FRAMMENTO IP DELL'HOST CHE OSPITA UN FRAMMENTO\n4 DATO NUME FILE IP DEGLI HOST SU CUI SONO SALVATI DEI FRAMMMENTI\n")
        if (mex == "exit"):
            break 
        s_client.sendall(mex.encode())
    s_client.close()

if __name__=="__main__":
    main()