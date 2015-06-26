import socket
import sys
sys.path.insert(0, '../..')
from simple_observer import Observer, Observable
import select

def plugin_main(parameter, observable):
    host = 'localhost'
    port = int(parameter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    outsocks = [sock]
    obs = Observer(observable)

    while True:
        read,write,exce = select.select([], outsocks, [])
        
        for w in write:
            if w == sock:
                conn, address = sock.accept()
                outsocks.append(conn)
                
            else:
                data = obs.wait()
                w.send(data)

    sock.close()
