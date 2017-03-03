'''
Created on 3 Feb 2017

@author: tanumoy chakraborty
'''
from django.db import models

class environment_list_manager(models.Manager):
    def create_environment_list(self,app_list,env):
        environment_list = self.create(app_list=app_list, env=env)
        return environment_list 