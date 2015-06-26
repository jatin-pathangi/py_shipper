import socket
import Queue
import time
import select

def plugin_main(parameter, queue):
    host = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(parameter)
    sock.bind(('localhost', port))
    sock.listen(5)
    insock = [sock]
 
    while True:
        inready, outready, excpetready = select.select(insock, [], [])
        
        for s in inready:

            if s == sock:
                client, addr = sock.accept()
                insock.append(client)
                
            else:    
                data = s.recv(1024)
                queue.put(data)
        
        time.sleep(5)
