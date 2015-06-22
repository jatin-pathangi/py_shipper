import json
import imp
import threading
from multiprocessing import Queue, Process, Lock
import threading
import Queue

pluginfolder = './plugins'
lock = threading.Lock()

def get_plugin(typ, category):
    cat = category + 's'
    os.chdir(os.path.join(pluginfolder, cat))
    dirlist = os.listdir(os.getcwd())
    if not typ + '.py' in dirlist:
        raise ValueError("Specified plugin type is not present")
    
    for i in dirlist:
        mod_name, mod_ext = os.path.splitext(i)
        if typ == mod_name:
            location = os.path.join(os.getcwd(), i)
            break
    
    mod = imp.load_source(typ+'.py', location)
    return mod

def thread_fn(data, cat, *args):
    try:
        mod = get_plugin(data["type"], cat)
    except ValueError:
        print 'Plugin type not present', data["type"]
        os._exit(0)
    
   res = mod.plugin_main(data["parameters"], *args)
   os._exit(0)

def main_child(process_queue, process_lock, config_data):
    data = process_queue.get()]
    n_threads = 2
    for i in xrange(len(config_data["output"])):
        n_threads += 1
    threads = []
    j = 0
    in_fil_queue = Queue.Queue()
    fil_out_queue = Queue.Queue()

    for j in xrange(n_threads):
        if j == 0:
            threads.append(threading.Thread(target=thread_fn, args=(config_data["input"], "input", in_fil_queue)))

        elif j == 1:
            threads.append(threading.Thread(target=thread_fn, args=(config_data["filter"], "filter", in_fil_queue, fil_out_queue)))

        else:
            threads.append(threading.Thread(target=thread_fn, args=(config_data["output"][j - 2], "output", fil_out_queue)))
        
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
