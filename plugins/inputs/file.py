import Queue
import os
import time

def plugin_main(parameter, queue):
    try:
        f = open(parameter, 'r')
    except IOError:
        print 'File not found'
        os._exit(0)
    
    t = 0
    while True:
        statinfo = os.stat(parameter)
        if statinfo.st_mtime > t:
            t = statinfo.st_mtime
            line = f.readline()
            queue.put(line)
        time.sleep(5)
