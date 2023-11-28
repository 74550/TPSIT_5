import socket as sck

my_address = ("127.0.0.1", 8000)  #IP = 0.0.0.0, identifica il mio computer

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

    s.bind(my_address)  #Metodo da richiamare solo su programmi server

    while True:
        text_received, address = s.recvfrom(4096)
        print(f"Ricevuto {text_received.decode()} da {address}")
        s.sendto(b"OK", address)

    s.close()

if __name__ == "__main__":
    main()