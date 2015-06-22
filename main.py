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

def main_child(process_queue, process_lock, config_data):
    data = process_queue.get()]
    n_threads = 2
    for i in range(len(config_data["output"])):
        n_threads += 1
    threads = []
    j = 0
    for j in xrange(n_threads):
        if j == 0:
            threads.append(threading.Thread(target=thread_fn, args=(config_data["input"])))

        elif j == 1:
            threads.append(threading.Thread(target=thread_fn, args=(config_data["filter"])))

        else:
            threads.append(threading.Thread(target=thread_fn, args=(config_data["output"])))
        
        threads[j].start()
    
    for thread in threads():
        thread.join()

    os._exit(0)
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
        processes.append(Process(target=main_child, args=(process_queue,process_lock, config_data[i])))
        processes[i].start()
        i += 1

    for process in processes:
        process.join()
