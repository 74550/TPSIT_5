from email.mime import message
import socket as sck
import time
from threading import Thread

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

SERVER = ('127.0.0.1',5000)


class ThreadMess(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            message=s.recv(4096).decode()
            print(message)

            

def main():
    s.connect(SERVER)
    t2= ThreadMess()
    t2.start()

    while True:
        nome = input('inserirsci nome file: ')
        mex = f'{nome}'.encode()
        #invio mex
        s.sendall(mex)
        risultato = s.recv(4096).decode() # mex decodificato in ascii 
        print(risultato)
    s.close()




if __name__ == '__main__':
    main()