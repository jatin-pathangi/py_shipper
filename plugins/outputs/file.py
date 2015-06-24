import Queue
import time

def plugin_main(parameter, queue):
    f = open(parameter, 'r')
    while True:
        data = queue.get()
        f.write(data+'\n')
        time.sleep(5)

    os._exit(0)
