import pickle
import socket
import sys
import threading

import rsa

self_host: str = ""
self_port: int = 0
self_username: str = ""
self_key: tuple[int, int] = (0, 0)

peers = []

server_thread = None
recv_queue = []


def server_thread_func(sock: socket.socket, root):
    while True:
        conn, (host, port) = sock.accept()
        username, msg = conn.recv(4096).decode().split(' ')
        peer = next((x for x in peers if x[2] == username), None)
        if not peer:
            print(f"Unknown incoming connection from {host}:{port} with username {username}")
            conn.close()
            continue

        #msg = rsa.decrypt(peer[3], rsa.decrypt(self_key, int(msg)))
        msg = rsa.decrypt(self_key, int(msg))
        msg = msg.to_bytes(4096, 'little').rstrip(b'\0')

        delta = pickle.loads(msg)
        recv_queue.append(delta)
        root.event_generate("<<RecvUpdate>>")

        conn.close()


def init(outpeers, root):
    global self_host
    global self_port
    global self_username
    global self_key
    global peers

    peers = outpeers

    configfile = open(sys.argv[1])
    (self_host, self_port, self_username, key, n) = configfile.readline()[:-1].split(' ')
    self_port = int(self_port)
    self_key = (int(key), int(n))
    for line in configfile.readlines():
        (host, port, username, key, n) = line[:-1].split(' ')
        port = int(port)
        key = (int(key), int(n))

        peers.append([host, port, username, key])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((self_host, self_port))
    server.listen()

    # global server_thread
    server_thread = threading.Thread(target=server_thread_func, args=(server, root))
    server_thread.start()


def sync(msg: bytes):
    for peer in peers:
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsock.connect((peer[0], peer[1]))
        cleartext = int.from_bytes(msg, 'little')
        # sign
        #ciphertext = rsa.encrypt(self_key, cleartext)
        # encrypt
        ciphertext = rsa.encrypt(peer[3], cleartext)
        clientsock.send((self_username + ' ' + str(ciphertext)).encode())
        clientsock.close()


def uninit():
    if server_thread:
        server_thread.stop()
