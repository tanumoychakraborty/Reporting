'''
Created on 10 Jan 2017

@author: tanumoy chakraborty
'''
import collections
from datetime import datetime

from dashboard.models import test_job_app, pipeline_opco
from jenkins_monitor.__main__ import logger
from jenkins_monitor.daemon_ops import j_process
from jenkins_monitor.stopwatch import StopWatch


def start():
    logger.info("Reading all job list")
    job_app = test_job_app.objects.all()
    q = collections.deque()
    c = 0
    for job in job_app:
        c+=1
        pipeline = pipeline_opco.objects.get(test_job_app=job)
        logger.info("Putting "+job.test_job_url+" for "+job.app+" in queue")
        q.append({"job":job, "pipeline_url":pipeline.pipeline_url, "stopwatch":datetime.now()})
    proc = j_process(q)
    proc.start()
    #proc.join()
    
