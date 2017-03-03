'''
Created on 28 Dec 2016

@author: tanumoy chakraborty
'''

from dashboard.models import latest_build, build_archive
from jenkins_monitor.__main__ import logger
from jenkins_monitor.jHelperClass import jHelperClass
from jenkins_monitor.jenkins_lib import get_job_info, get_builds
from jenkins_monitor.model_handler import get_latest_build_by_url


class read_j:
    
    def __init__(self, job_url, app, pipeline_url):
        self.job_url = job_url
        self.app = app
        self.pipeline_url = pipeline_url
        self.buildsNotSaved = []
        self.hasNewBuild = False
    
    def syncJob(self):
        self.hasNewBuild, self.buildsNotSaved = self.lookForNewBuilds()
        if self.hasNewBuild:
            __j__ = jHelperClass(self.app, self.buildsNotSaved, self.pipeline_url)
            saved = __j__.saveNewBuilds()
            if reduce(lambda x,y: x and y, saved):
                return 1
            else:
                return -1
        else:
            return 0
    
    
    def lookForNewBuilds(self):
        details = get_job_info(self.job_url)
        builds = get_builds(details)
        jLatestBuild = builds[0]['number']
        try:
            dLatestBuild = get_latest_build_by_url(self.job_url)
        except (build_archive.DoesNotExist, latest_build.DoesNotExist):
            logger.info("no entry found for the build " + self.job_url)
            return True, builds
        if jLatestBuild == dLatestBuild:
            return False, None
        else:
            __bns__ = map(lambda x: x if int(x['number']) > dLatestBuild else None, builds)
            buildsNotSaved = filter(None, __bns__)
            return True, buildsNotSaved
    
