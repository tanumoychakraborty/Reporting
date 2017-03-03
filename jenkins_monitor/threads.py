'''
Created on 17 Jan 2017

@author: tanumoy chakraborty
'''
import threading

from jenkins_monitor.ReadJenkins import read_j
from jenkins_monitor.test import logger


class t_maker(threading.Thread):
    
    def __init__(self, threadID, b, name="no name"):
        threading.Thread.__init__(self)
        self.dad = b
        self.threadID = threadID
        self.name = name
        self.task = {}
        self.busy = False
#        self.daemon = True
        
    def run(self):
        logger.info("Thread "+self.name + " in the house..")
        while True:
            self.busy = True
            self.askForTask()
            logger.info("Thread " + self.name + " reading " + self.task['job'].test_job_url)
            __j__ = read_j(self.task['job'].test_job_url, self.task['job'].app, self.task['pipeline_url'])
            code = __j__.syncJob()
            if code == 1:
                logger.info("Thread " + self.name + " says saved all builds for job "+self.task['job'].test_job_url) 
            if code == -1:
                logger.info("Thread " + self.name + " says could not save all builds for job "+self.task['job'].test_job_url)
            if code == 0:
                logger.info("Thread " + self.name + " says build Details already up to date for "+self.task['job'].test_job_url)
            
            self.busy = False
        
    def askForTask(self):
        logger.info("Thread " + self.name + " asking for work")
        self.task = self.dad.get_work()