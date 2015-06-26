"""
This is a very simple and basic implementation of the observer pattern
Instances of the class Observable() can be observed by multiple instances 
of the class Observer().
"""

import Queue

class Observable:
    def __init__(self):
        self.__observers = []
    
    """
    Observer instances call this function on the observable instance in their
    argument to observe the particular observable
    """

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, data):
        for observer in self.__observers:
            observer.notify(self, data)

class Observer:
    def __init__(self, observable):
        observable.register_observer(self)
        self.queue = Queue.Queue()
    
    """
    This function is called by the observable instance in the argument. The data is 
    put into a local queue in order to make the observer synchronous.
    """
    def notify(self, observable, data):
        self.queue.put(data)

    """Blocking function that waits until notify() has put data into a local queue"""
    def wait(self):
        data = self.queue.get()
        return data
