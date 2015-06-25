import sys
sys.path.insert(0,'../..')
from simple_observer import Observer, Observable
import time

class Outobserver(Observer):
    def notify(self, observable, *args, **kwargs):
        return args

def plugin_main(parameter, observable):
    f = open(parameter, 'r')
    obs = Outobserver(observable)
  
