from sys import argv
from threading import Thread
import socket

if len(argv) != 3:
    print("Usage: python -m server [host] [port]")
    exit(1)

host, port = argv[1], int(argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

active_connections = {}

server.listen(100)

def on_connection(connection,usr):
    while True:
        try:
            msg = connection.recv(1024).decode()
            for user in active_connections.keys():
                if usr == user:
                    continue
                else:
                    active_connections[user].send(f"<{usr}>: {msg}".encode())
        except:
            connection.close()
            del active_connections[usr]
            break

while True:
    connection, addr = server.accept()
    usr = connection.recv(1024).decode()
    active_connections[usr] = connection
    Thread(target=on_connection, args=(connection,usr)).start()

server.close()