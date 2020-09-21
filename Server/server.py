import socket
import os
import sys
import tqdm


host = 'localhost'
port = 7771
addr = (host, port)
server = socket.socket()
server.bind(addr)
server.listen(1)


def main():
    global server,host,port,addr
    
    BUFFER_SIZE = 4096
    SEPARATOR="<MyavMyav>"
    print(f"[*] Listening as {host}:{port}")
    client_socket, address = server.accept()
    print(f"[+] {address} is connected.")

    
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    files = os.listdir(".")
    filen = filename.split(".")
    if filename in files:
        i = 1
        filename = filen[0] + f"_copy{i}." + filen[1]
    while filename in files:
        i += 1
        filename = filen[0] + f"_copy{i}." + filen[1]
    filesize = int(filesize)

    print ('Received data: ' , filename)
    print ('From: ' , address)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                progress.close()
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    client_socket.close()

    
if __name__ == '__main__':
    while True:
        main()
