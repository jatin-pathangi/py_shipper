import socket
import Queue

def plugin_main(parameter, queue):
    host = 'localhost'
    port = int(parameter)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(host, port)
    sock.listen(5)
    outsocks = [sock]

    while True:
        read,write,exce = select.select([], outsocks, [])
        
        for w in write:
            if w == sock:
                conn, address = sock.accept()
                write.append(conn)
                
            else:
                data = queue.get()
                conn.send(data)

    sock.close()
    os._exit(0)
