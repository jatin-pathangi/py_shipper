import sys
sys.path.insert(0,'../..')
from simple_observer import Observer, Observable
import time

def plugin_main(parameter, observable):
    f = open(parameter, 'r')
    obs = Outobserver(observable)
    while True:
        data = obs.wait()
        f.write(data + '\n')

    f.close()
  
