import json
import imp
import threading
from multiprocessing import Queue, Process, Lock
import threading

pluginfolder = './plugins'
conf = open('config.json', 'r')
lock = threading.Lock()

def get_plugin(typ, category):
    os.chdir(os.path.join(pluginfolder, category))
    dirlist = os.listdir(os.getcwd())
    if not typ + '.py' in dirlist:
        raise ValueError("Specified plugin type is not present")
    
    for i in dirlist:
        mod_name, mod_ext = os.path.splitext(i)
        if typ == mod_name:
            location = os.path.join(os.getcwd(), i)
            break
    
    mod = imp.load_source(typ, location)
    return mod

def call_plugin(typ, category, *args, **kwargs):
    get_plugin(typ, category)
    plugin_main(*args, **kwargs)

def main_child(process_queue, process_lock):
    process_lock.acquire()
    data = process_queue.get()
    process_lock.release()
    thread_lock = threading.Lock()


def main_parent():
    process_queue = Queue()
    process_lock = Lock()
    i = 0
    f = open("config.json", 'w')
    config_data = json.load(f)
    f.close()
    processes = []
    for item in config_data:
        process_queue.put(item)

    for item in config_data:
        processes.append(Process(target=main_child, args=(process_queue,process_lock)))
        processes[i].start()
        i += 1

    for process in processes:
        process.join()
