import json
import imp
import threading
from multiprocessing import Queue, Process, Lock
import threading
import Queue as queue
from simple_observer import Observable, Observer
import os

"""
The plugin folder can be renamed to suit your need
"""
pluginfolder = '/Users/jatin1/py_shipper/plugins'
lock = threading.Lock()

"""
Function to get a specified plugin from the plugin folder
The plugin type to get is specified by the arguments
"""

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

"""
Following is the function that is executed by the worker threads
The specific type of the thread function i.e input, output or
filter, is specified by the argument 'cat'. Rest of the arguments
are the queue and/or the observable object instance
"""

def thread_fn(data, cat, *args):
    try:
        lock.acquire()
        m = get_plugin(data["type"], cat)
        lock.release()
    except ValueError:
        print 'Plugin type not present', data["type"]
        os._exit(0)

    """
    Every plugin has a function called plugin_main() which is called 
    here after the module has been loaded
    """
    res = m.plugin_main(data["parameters"], *args)
 
 """
Everytime a new process is created by the main parent function, the 
following function is executed by that child. 
 """

def main_child(process_queue, process_lock, config_data):
    data = process_queue.get()
    n_threads = 2
    for i in xrange(len(config_data["output"])):
        n_threads += 1
    threads = []
    j = 0
    in_fil_queue = queue.Queue()
    
    """
    This is an instance of the Observable() class which can be 'Observed' by multiple
    observers. In this case, a filter plugin will publish data to this subject which will
    be recieved by any 'observers' in this case output plugins, who are 'observing' this
    particular Observable() instance
    """

    filter_to_output = Observable()

    """
    Threads are created for each type: one thread each to process input and
    to convert it using an appropriate filter, and one thread each for the 
    list of outputs. Each output thread can subscribe or observe the Observable()
    'filter_to_output' and recieve data whenever it is published by a filter, which 
    it can then take appropriate action on, like writing the data to a file or sending 
    it to a client listening on a particular port.
    """

    for j in xrange(n_threads):
        if j == 0:
            threads.append(threading.Thread(target=thread_fn, 
                           args=(config_data["input"], 
                           "input", 
                           in_fil_queue
                           )))
        elif j == 1:
            threads.append(threading.Thread(target=thread_fn, 
                           args=(config_data["filter"],
                           "filter", 
                           in_fil_queue, 
                           filter_to_output
                           )))
        else:
            threads.append(threading.Thread(target=thread_fn, 
                           args=(config_data["output"][j - 2], 
                           "output", 
                           filter_to_output
                           )))
        
        threads[j].start()
    
    for thread in threads:
        thread.join()

"""
This is the main driver function that is executed when the program is invoked. This function 
first opens the 'config.json' file and then spwans a new process for every element in that file.
Each element in the 'config.json' file consists of the appropriate plugins to be loaded for each 
of the three categories, input, filter and output. In essence, each process is a log shipper for 
an input which can be converted via a filter, and passed to two or more outputs
"""

def main_parent():
    process_queue = Queue()
    process_lock = Lock()
    i = 0
    f = open("config.json", 'r')
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

main_parent()
