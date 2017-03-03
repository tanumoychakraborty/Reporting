'''
Created on 13 Jan 2017

@author: tanumoy chakraborty
'''
import multiprocessing
import time

from jenkins_monitor.__main__ import logger
from jenkins_monitor.pickling import save_daemon_process_id
from jenkins_monitor.threads import t_maker


class j_process(multiprocessing.Process):
    
    def __init__(self,q):
        logger.info("Forking process to read jenkins")
        super(j_process, self).__init__()
        self.name = "j_daemon_"
        self.daemon = True
        self.q = q     
        self.thread_list = []
        
    def get_work(self):
        work = self.q.popleft()
        self.q.append(work)
        return work           
    
    def run(self):
        logger.info("started process j_daemon with id "+ str(self.pid))
        #path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"j_daemon")
        process_info = {self.pid:self.name}
        #with open (path, 'wb') as fp:
        #    pickle.dump(process_info,fp)
        save_daemon_process_id(process_info)
        __q_len = len(self.q)
        '''
        till db connection pooling is done
        
        __t_count = 10 if __q_len > 10 else __q_len
        '''
        __t_count = 1
        self.createPool(__t_count)
        self.fire()
        self.waitForThreads()
        logger.info("All threads are DADE .... The process is exiting")
                    
    
    def createPool(self,__t_count):
        logger.info("Creating thread pool of size "+str(__t_count))
        for _ in range(__t_count) :
            self.thread_list.append(t_maker(_+65, self, "thread_"+str(_)))
        
    
    def fire(self):
        for t in self.thread_list:
            logger.info("firing thread " + t.name)
#            t.daemon = True
            t.start()
#        map(lambda t: t.start(), self.thread_list)

    def waitForThreads(self):
        while any(t.isAlive() for t in self.thread_list):
            logger.info("Checking heartbeat .... All threads are alive")
            time.sleep(10)
            
