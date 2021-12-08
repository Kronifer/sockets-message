from sys import argv, stdin, stdout
import socket
from threading import Thread

if len(argv) != 3:
    print("Usage: python -m client <server> <port>")
    exit(1)

server, port = argv[1], int(argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((server, port))

usr = input("Username: ")

client.sendall(usr.encode())

def recieve_msg(conn):
    while True:
        try:
            msg = conn.recv(1024)
            stdout.write(msg.decode())
        except:
            break

def send_msg(conn):
    while True:
        msg = stdin.readline()
        if msg == "/quit\n":
            stdout.write("Bye\n")
            client.close()
            break
        conn.sendall(msg.encode('utf-8'))
        print(f"<You>: {msg}")

Thread(target=recieve_msg, args=(client,)).start()
Thread(target=send_msg, args=(client,)).start()
