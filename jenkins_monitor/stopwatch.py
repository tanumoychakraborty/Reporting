'''
Created on 6 Mar 2017

@author: tanumoy chakraborty
'''
import threading
import time


class StopWatch(threading.Thread):
    '''
    This is a simple thread that will count seconds once it is triggered.
    It has a reset method to reset the timer to start counting from zero again.
    The interval is the time unit with which it will count
    '''


    def __init__(self, t, intrvl = 1):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = "stopwatch # " + str(t)
        self.interval=intrvl
        self.stopwatch_count = 0
        self.started=False
        
    
    def run(self):
        self.started=True
        while self.started:
            time.sleep(self.interval)
            self.stopwatch_count = self.stopwatch_count + self.interval
            
    
    def hasStarted(self):
        return self.started
    
    
    def reset(self):
        self.stopwatch_count = 0
        
    
    def getStopwatchCount(self):
        return self.stopwatch_count        
    
    
    def stop(self):
        self.started=False
        return self.stopwatch_count        