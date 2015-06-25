from simple_observer import Observer, Observable
import threading
import time
import os

def f(sub):
    observ = Observer(sub)
    data = observ.wait()
    print data
  
def fn2(sub):
    sub.notify_observers('hi')

def main():
    subject = Observable()
    th = []
    for i in xrange(5):
        th.append(threading.Thread(target=f, args=(subject,)))
        th[i].start()
    t = threading.Thread(target=fn2, args=(subject,))
    t.start()
    t.join()
    for y in th:
        y.join()

main()
