import sys
sys.path.insert(0,'../..')
from simple_observer import Observer, Observable
import time

def plugin_main(parameters, queue, observable):
    while True:
        queue.get()
        observable.notify_subscribers(data)
        time.sleep(5)
