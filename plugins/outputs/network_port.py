import socket
import sys
sys.path.insert(0, '../..')
from simple_observer import Observer, Observable
import select
import time

def plugin_main(parameter, observable):
    host = 'localhost'
    port = int(parameter)
    obs = Observer(observable)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    
    while True:
        data = obs.wait()
        sock.send(data)
        time.sleep(3)
            
    sock.close()           
