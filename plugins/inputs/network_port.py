import socket
import Queue
import time

def plugin_main(parameter, queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(parameter)
    sock.connect(('localhost', port))
    while True:
        data = sock.recv(1024)
        queue.put(data)
        time.sleep(5)
