import socket as sck

SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFSIZE = 4096

def main():
    client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    client.connect(SERVER_ADDRESS)

    operations_list = client.recv(BUFSIZE).decode().split(";")
    results = ""
    for operation in operations_list:
        print(operation)
        results += f"{eval(operation)};"
    client.sendall(results[:-1].encode())

    message_to_exit = client.recv(BUFSIZE).decode()

    if message_to_exit == "exit":
        client.close()

if __name__ == "__main__":
    main()