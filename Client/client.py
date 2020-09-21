import socket
import sys
import os
import tqdm


file = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])
addr = (host, port)
filesize = os.path.getsize(file)
client = socket.socket()
BUFFER_SIZE = 4096


print(f"[+] Connecting to {host}:{port}")
client.connect((host, port))
print("[+] Connected.")
SEPARATOR="<MyavMyav>"
client.send(f"{file}{SEPARATOR}{filesize}".encode())


progress = tqdm.tqdm(range(filesize), f"Sending {file}", unit_scale=True, unit_divisor=1024)
with open(file, "rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            progress.close()
            break
        client.sendall(bytes_read)
        progress.update(len(bytes_read))

client.close()
