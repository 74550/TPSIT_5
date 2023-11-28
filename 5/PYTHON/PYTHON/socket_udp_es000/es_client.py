"""
Version = 4
Header lenght = 20 bytes (5)
Total lenght = 32
Identification = 0xba95 (47765)
Time to live = 128
Protocol = UDP (17)
Header Checksum: 0x0000
Source address = 127.0.0.1
Destination address = 127.0.0.1



Source port = 58287
Destination port = 8000
Lenght = 12
Checksum = 0x3a0b [unverified]
UDP payload = 4 bytes

Data = 6369616f
"""


import socket as sck

server_address = ("127.0.0.1", 8000)

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

    while True:
        text = input("Inserire un messaggio: ")

        if text == "EXIT":
            break

        text_b = text.encode()
        s.sendto(text_b, server_address)
        text_received, address = s.recvfrom(4096)
        print(f"Ricevuto {text_received.decode()} da {address}")
    
    s.close()

if __name__ == "__main__":
    main()