import Queue

class Observable:
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, data):
        for observer in self.__observers:
            observer.notify(self, data)

class Observer:
    def __init__(self, observable):
        observable.register_observer(self)
        self.queue = Queue.Queue()

    def notify(self, observable, data):
        self.queue.put(data)

    def wait(self):
        data = self.queue.get()
        return data
