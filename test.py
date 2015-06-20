from multiprocessing import Process, Queue, Lock
import json

def child(q, l):
    l.acquire()
    data = q.get()
    print data
    l.release()

def parent():
    q = Queue()
    l = Lock()
    f = open('config.json', 'r')
    d = json.load(f)
    f.close()
    p = []
    i = 0
    for item in d:
        q.put(item)
    
    for item in d:
        p.append(Process(target=child, args=(q,l)))
        p[i].start()
        i += 1
    
    for x in range(len(p)):
        p[x].join()


parent()
