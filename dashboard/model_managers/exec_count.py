'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''

from django.db import models

class exec_count_manager(models.Manager):
    def create_exec_count(self,count,env_opco_app):
        exec_count = self.create(count=count, env_opco_app=env_opco_app)
        return exec_count