import sys
sys.path.insert(0,'../..')
from simple_observer import Observer, Observable
import time
import Queue

def plugin_main(parameters, queue, observable):
    while True:
        data = queue.get()
        observable.notify_subscribers(data)
        time.sleep(2)
