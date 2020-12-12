import socket
import tqdm
import os
# device's IP address
HOST = "192.168.0.117"
PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = " "

# create the server socket
# TCP socket
s = socket.socket()
s.bind((HOST, PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

client_socket.close()
s.close()

