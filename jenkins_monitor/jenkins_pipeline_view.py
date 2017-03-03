'''
Created on 22 Feb 2017

@author: tanumoy chakraborty
'''
from jenkins_monitor.jenkins_lib import getPipelinePrimaryView, getViewInfo, \
    getJobDisplayName


class PipelineView():
    def __init__(self,url):
        self.jobs = []
        self.pipeline_url = url
        self.stages = []
        self.stages_dict = {}
        self.first_job = ""
    
    
    def setPrimarytViewToUrl(self):
        __ppv__ = getPipelinePrimaryView(self.pipeline_url)
        if self.pipeline_url.endswith("/"):
            self.pipeline_url += "view/"+__ppv__['primaryView']['name']
        else :
            self.pipeline_url += "/view/"+__ppv__['primaryView']['name']
        
            
    def setViewInfo(self):
        __info__ = getViewInfo(self.pipeline_url)
        __ppln__ = __info__['pipelines'][0]
        self.first_job = __ppln__['firstJob']
        for _ in __info__['jobs']:
            if self.first_job == _['name']:
                self.first_job = _['name'] = getJobDisplayName(_['url'])
            else :
                _['name'] = getJobDisplayName(_['url'])
            self.jobs.append(_)
        self.stages = __ppln__['pipelines'][0]['stages']
    
    def replicatePipelineView(self):
        self.setPrimarytViewToUrl()
        self.setViewInfo()
        for stage in self.stages:
            __pj__ = filter(lambda x: x['name'] == stage['name'], self.jobs)
            stage['color'] = __pj__[0]['color']
            stage['url'] = __pj__[0]['url']
            self.stages_dict[stage['name']] = stage
        
        return self.first_job, self.stages_dict
    