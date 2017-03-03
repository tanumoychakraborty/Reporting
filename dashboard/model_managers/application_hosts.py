'''
Created on 20 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models

class application_host_manager(models.Manager):
    def create_application_host(self,host,env_opco_app):
        application_host = self.create(host=host, env_opco_app=env_opco_app)
        return application_host    